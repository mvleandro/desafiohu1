/**
 * Avail.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {
  	hotelId: {
	    type: 'integer',
	    defaultsTo: 0
	},
	date: {
	    type: 'date',
	    defaultsTo: null
	},
	available: {
	    type: 'boolean',
	    defaultsTo: 0
	},
	minNight: {
	    type: 'integer',
	    defaultsTo: 0
	},
  }
};

