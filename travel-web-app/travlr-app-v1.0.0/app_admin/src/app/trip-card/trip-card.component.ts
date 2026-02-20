import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
// Required for Angular to route the component
import { Router } from '@angular/router';
// Provides easy access to data fields in editTrip method
import { Trip } from '../models/trip';
import { AuthenticationService } from '../services/authentication.service'; 

@Component({
  selector: 'app-trip-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './trip-card.component.html',
  styleUrl: './trip-card.component.css'
})

export class TripCardComponent implements OnInit {

  // Input directive allows trip-listing component
  // to pass 'trip' data to render instance of a trip
  @Input('trip') trip: any;

  // Binds the imported Router object
  constructor(
    private router: Router,
    private authenticationService: AuthenticationService
  ) {}

  ngOnInit(): void {}

  public editTrip(trip: Trip) {
    // Local browser storage to set tripCode variable for later use
    localStorage.removeItem('tripCode');
    localStorage.setItem('tripCode', trip.code);
    this.router.navigate(['edit-trip']);
  }

  public isLoggedIn() 
  { 
    return this.authenticationService.isLoggedIn(); 
  }
}
