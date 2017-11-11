/**
 * Bootstrap
 * (sails.config.bootstrap)
 *
 * An asynchronous bootstrap function that runs before your Sails app gets lifted.
 * This gives you an opportunity to set up your data model, run jobs, or perform some special logic.
 *
 * For more information on bootstrapping your app, check out:
 * http://sailsjs.org/#!/documentation/reference/sails.config/sails.config.bootstrap.html
 */

module.exports.bootstrap = function(cb) {

  	//Reading CSV and saving data
  	//using the sails ORM
  	sails.fastcsv = require('fast-csv');
  	
  	const fs = require('fs');
  	
  	//Removing all data
  	Hotel.destroy({}).exec(function (err) {});
  	Place.destroy({}).exec(function (err) {});
  	Avail.destroy({}).exec(function (err) {});
  
  	//Reading hotels
  	var streamHotel = fs.createReadStream("../../../artefatos/hoteis.txt");
 
	var csvHotelStream = sails.fastcsv()
	    .on("data", function(data){

	    	 Hotel.create({
	    	 	"id":data[0],
	    	 	"name":data[2],
	    	 	"city":data[1]
	    	 	}).exec(function createCB(err, created){
	    	 		if (created != null) {
						console.log('Created hotel with name ' + created.name);
					}
				});

	    })
	    .on("end", function(){
	         console.log("done");
	    });

	streamHotel.pipe(csvHotelStream);

	//Reading places
  	var streamPlace = fs.createReadStream("../../../artefatos/hoteis.txt");
 
	var csvPlaceStream = sails.fastcsv()
	    .on("data", function(data){

			 //Create a hotel
	    	 Place.create({
	    	 	"key":data[0],
	    	 	"name":data[2],
	    	 	"type":1,
	    	 	}).exec(function createCB(err, created){
	    	 		if (created != null) {
						console.log('Created hotel with name ' + created.name);
					}
				});

			//check if place exists
			var placeExists = false;				

			Place.find({
				name : {'contains' : data[1]}
				}).exec(function createCB(err, data){						
					placeExists = data != null;
				});

			if(!placeExists)
			{
				//Create a place
				Place.create({
					"key":0,
					"name":data[1],
					"type":2,
					}).exec(function createCB(err, created){
						if (created != null) {
							console.log('Created place with name ' + created.name);
						}
					});
			}
	    })
	    .on("end", function() {
	         console.log("done");
	    });

	streamPlace.pipe(csvPlaceStream);

	//Reading available
	var streamAvail = fs.createReadStream("../../../artefatos/disp.txt");

	var csvAvailStream = sails.fastcsv({ headers: true })
	    .on("data", function(data){


			var dateParts = data[1].split('/');
			
	    	 Avail.create({
	    	 	"hotelId":data[0],
	    	 	"date": new Date(dateParts[2],dateParts[1]-1, dateParts[0]),
				"available":data[2]==1?true:false,
				"minNight": data[3]
	    	 	}).exec(function createCB(err, created){
					if (created != null) {
						console.log('Created availbility for hotelId ' + created.hotelId + ' at date ' + created.date);
					}
				});

	    })
	    .on("end", function(){
	         console.log("done");
	    });

	streamAvail.pipe(csvAvailStream);

  	cb();

};