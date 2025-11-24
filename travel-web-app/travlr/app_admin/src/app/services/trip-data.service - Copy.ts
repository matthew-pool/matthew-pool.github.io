// Provides access via injection
import { Inject, Injectable } from '@angular/core';
// Handles HTTP requests
import { HttpClient } from '@angular/common/http';
// Handles async calls
import { Observable } from 'rxjs';
// Model used for data format
import { Trip } from '../models/trip';  
// Handles email and name params
import { User } from '../models/user';
// Observable type returned from logain and register
import { AuthResponse } from '../models/auth-response';
// Provides access to persistent data
import { BROWSER_STORAGE } from '../storage';

@Injectable({
  providedIn: 'root'
})

// HTTP connection in the service is asynchronous
export class TripDataService {

  constructor(
    private http: HttpClient,
  @Inject(BROWSER_STORAGE)
    private storage: Storage
  ) {}
  
  baseUrl = 'http://localhost:3000/api';
  url = 'http://localhost:3000/api/trips';

   // Call to our /login endpoint, returns JWT 
   login(user: User, passwd: string) : Observable<AuthResponse> { 
    // console.log('Inside TripDataService::login'); 
    return this.handleAuthAPICall('login', user, passwd); 
  } 
 
  // Call to our /register endpoint, creates user and returns JWT 
  register(user: User, passwd: string) : Observable<AuthResponse> { 
    console.log('Inside TripDataService::register'); 
    return this.handleAuthAPICall('register', user, passwd); 
  } 
 
  // Helper method to process login and register methods 
  handleAuthAPICall(endpoint: string, user: User, passwd: string) : 
  Observable<AuthResponse> { 
    console.log('Inside TripDataService::handleAuthAPICall'); 
    let formData = { 
      name: user.name, 
      email: user.email, 
      password: passwd 
    }; 
    return this.http.post<AuthResponse>(this.baseUrl + '/' + endpoint, formData); 
  }

  // Returning an Observable object allows the component
  // to attach to the object and get a notification when the
  // async call is completed and the associated promise fulfilled
  getTrips() : Observable<Trip[]> {
    return this.http.get<Trip[]>(this.url);
  }

  addTrip(formData: Trip) : Observable<Trip> {
    return this.http.post<Trip>(this.url, formData);
  }

  getTrip(tripCode: string) : Observable<Trip[]> {
    console.log('Inside TripDataService::getTrips');
    return this.http.get<Trip[]>(this.url + '/' + tripCode);
  }

  updateTrip(formData: Trip) : Observable<Trip> {
    console.log('Inside TripDataService:addTrips');
    return this.http.put<Trip>(this.url + '/' + formData.code,formData);
  }


}
