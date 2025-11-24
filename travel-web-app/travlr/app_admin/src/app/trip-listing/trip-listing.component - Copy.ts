import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { trips } from '../data/trips';
// Allows trip-listing to recognize trip-card component
import { TripCardComponent } from '../trip-card/trip-card.component';
import { Trip } from '../models/trip';
import { TripDataService } from '../services/trip-data.service';
// Pulls in Angular routing capability
import { Router } from '@angular/router';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-trip-listing',
  standalone: true,
  imports: [CommonModule, TripCardComponent],
  templateUrl: './trip-listing.component.html',
  styleUrl: './trip-listing.component.css',
  // Register TripDataService as a provider
  providers: [TripDataService]
})

export class TripListingComponent implements OnInit {
  trips: Array<any> = trips;
  message: string = '';

  constructor(
    // Initialize
    private tripDataService: TripDataService,
    private router: Router,
    private authenticationService: AuthenticationService
  ) {
    console.log('trip-listing constructor');
  }

  // public function for trip-listing component
  public addTrip(): void {
    this.router.navigate(['add-trip']);
  }

  // Call getRip() in TripDataService
  private getStuff() : void {
    this.tripDataService.getTrips()
      .subscribe({
        next: (value: any) => { 
          this.trips = value; 
          if(value.length > 0) 
          { 
            this.message = 'There are ' + value.length + ' trips available.'; 
          } 
          else
          { 
            this.message = 'There were no trips retireved from the database'; 
          } 
          console.log(this.message); 
        }, 
        error: (error: any) => { 
          console.log('Error: ' + error); 
        } 
      })
  }

  public isLoggedIn() 
  { 
    return this.authenticationService.isLoggedIn(); 
  }

  ngOnInit(): void {
    console.log('ngOnInit');
    // Calls getStuff method when component is initialized
    this.getStuff();
  }
}
