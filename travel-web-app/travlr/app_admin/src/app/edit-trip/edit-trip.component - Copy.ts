import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from "@angular/forms";
import { Router } from "@angular/router"; 
import { TripDataService } from '../services/trip-data.service'; 
import { Trip } from '../models/trip';

@Component({
  selector: 'app-edit-trip',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './edit-trip.component.html',
  styleUrl: './edit-trip.component.css'
})

export class EditTripComponent implements OnInit {
  // Local variables to manipulate data
  public editForm!: FormGroup; 
  trip!: Trip; 
  submitted = false; 
  message : string = ''; 

  // Builds form, routes component, and pulls data from TripDataService
  constructor( 
    private formBuilder: FormBuilder, 
    private router: Router, 
    private tripDataService: TripDataService 
   ) {} 

   ngOnInit() : void {
    // Retrieve stashed trip ID
    let tripCode = localStorage.getItem("tripCode");
    if(!tripCode) {
      alert("Someething wrong, couldn't find where I stashed tripCode!");
      this.router.navigate(['']);
      return;
    }
    
    console.log('EditTripComponent::ngOnInit');
    console.log('tripcode:' + tripCode);

    this.editForm = this.formBuilder.group({ 
      _id: [], 
      code: [tripCode, Validators.required], 
      name: ['', Validators.required], 
      length: ['', Validators.required], 
      start: ['', Validators.required], 
      resort: ['', Validators.required], 
      perPerson: ['', Validators.required], 
      image: ['', Validators.required], 
      description: ['', Validators.required] 
    }) 
 
    this.tripDataService.getTrip(tripCode) 
      .subscribe({ 
        next: (value: any) => { 
          this.trip = value; 
          // Format date for populating date picker
          value[0].start = this.formatDate(value[0].start);
          // Populate our record into the form 
          this.editForm.patchValue(value[0]); 
          if(!value) 
          { 
            this.message = 'No Trip Retrieved!'; 
          } 
          else{ 
            this.message = 'Trip: ' + tripCode + ' retrieved'; 
          } 
          console.log(this.message); 
        }, 
        error: (error: any) => { 
          console.log('Error: ' + error); 
        } 
      }) 
    }

    // Helper method to format date to 'YYYY-MM-DD' for input[type="date"]
    private formatDate(date: string): string {
      const d = new Date(date);
      const month = ('0' + (d.getMonth() + 1)).slice(-2);
      const day = ('0' + d.getDate()).slice(-2);
      const formattedDate = `${d.getFullYear()}-${month}-${day}`;
      return formattedDate ;
    }

    public onSubmit() 
    { 
      this.submitted = true; 
   
      if(this.editForm.valid) 
      { 
        this.tripDataService.updateTrip(this.editForm.value) 
        .subscribe({
        next: (value: any) => { 
          console.log(value); 
          this.router.navigate(['']); 
        }, 
        error: (error: any) => { 
          console.log('Error: ' + error); 
        } 
      }) 
    } 
  } 

  // Get the form short name to access the form fields
  get f() { return this.editForm.controls; }
  
}
