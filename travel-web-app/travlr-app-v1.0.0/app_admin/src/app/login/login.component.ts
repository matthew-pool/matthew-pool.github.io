import { Component, OnInit } from '@angular/core'; 
import { CommonModule } from '@angular/common'; 
// Processes HTML form in the template
import { FormsModule } from "@angular/forms";
// Redirects user to another page after logging in 
import { Router } from '@angular/router'; 
// Processes user login
import { AuthenticationService } from '../services/authentication.service'; 
// Manipulates User credentials
import { User } from '../models/user';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {
  public formError: string = ''; 
  submitted = false; 
 
  credentials = { 
    name: '', 
    email: '', 
    password: '' 
  }

  constructor( 
    private router: Router, 
    private authenticationService: AuthenticationService 
  ) { } 
 
  ngOnInit(): void { }
  
  // Called when user clicks "Sign-In!" button
  public onLoginSubmit(): void { 
    this.formError = ''; 
    // Verify all parameters have data
    if (!this.credentials.email || !this.credentials.password || !this.credentials.name) { 
      // Error message and redirect to login page
      this.formError = 'All fields are required, please try again'; 
      this.router.navigateByUrl('#'); 
    } else { 
      // No error
      this.doLogin(); 
    } 
  }

  private doLogin(): void { 
    // Construct User object
    let newUser = { 
      name: this.credentials.name, 
      email: this.credentials.email 
    } as User; 
 
    console.log('LoginComponent::doLogin'); 
    console.log(this.credentials);
    // Calls login method 
    this.authenticationService.login(
      newUser, 
      this.credentials.password
    ); 
 
    // Verify user logged in
    if(this.authenticationService.isLoggedIn()) 
    { 
      console.log('Router::Direct'); 
      // Redirect to trip-list page
      this.router.navigate(['']); 
    // User not logged in
    } else { 
      // Hang for 3 seconds and check again
      // (due to potential async issues)
      var timer = setTimeout(() => { 
        if(this.authenticationService.isLoggedIn()) 
        { 
          console.log('Router::Pause'); 
          this.router.navigate(['']); 
        }},
        500
      ); 
    } 
  }

}
