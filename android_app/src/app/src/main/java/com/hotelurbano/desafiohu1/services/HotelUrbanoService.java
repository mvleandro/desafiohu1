package com.hotelurbano.desafiohu1.services;

import com.hotelurbano.desafiohu1.model.Hotel;
import com.hotelurbano.desafiohu1.model.Place;

import java.util.List;

import retrofit.Callback;
import retrofit.http.GET;
import retrofit.http.Query;

/**
 * Created by andrewbraga on 11/7/17.
 */
public interface HotelUrbanoService {

    @GET("/place/search")
    public void getPlaces(@Query("query") String query,
                          Callback<List<Place>> places);

    @GET("/hotel/check")
    public void getAvail(@Query("id") String id,
                         @Query("city") String city,
                         @Query("startDate") String startDate,
                         @Query("endDate") String endDate,
                         Callback<List<Hotel>> hotels);

}
