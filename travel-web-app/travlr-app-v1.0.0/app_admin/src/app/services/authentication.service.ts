// Manages access to Storage provider via injection
import { Inject, Injectable } from '@angular/core';
// Provides access to local Storage provider
import { BROWSER_STORAGE } from '../storage';
// Represents user data
import { User } from '../models/user';
// Represents JWTs
import { AuthResponse } from '../models/auth-response';
// Adds login and register endpoints
import { TripDataService } from './trip-data.service';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  // Setup storage and service access 
  constructor( 
    @Inject(BROWSER_STORAGE)
      private storage: Storage, 
      private tripDataService: TripDataService 
  ) { } 

  // Variable to handle Authentication Responses 
  authResp: AuthResponse = new AuthResponse();

  // Get token from Storage provider  
  public getToken(): string { 
    let out: any; 
    out = this.storage.getItem('travlr-token'); 
 
    // Return a string (with or without token)
    if(!out) 
    { 
      return ''; 
    } 
    return out; 
  } 
  
  // Save token to Storage provider
  public saveToken(token: string): void { 
    this.storage.setItem('travlr-token', token); 
  } 
 
  // Logout and remove JWT from Storage 
  public logout(): void { 
    this.storage.removeItem('travlr-token'); 
  }

  // Boolean determines if user is logged in with valid (unexpired) token 
  public isLoggedIn(): boolean { 
    const token: string = this.getToken(); 
    if (token) { 
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp > (Date.now() / 1000); 
    } else { 
      return false; 
    } 
  } 
 
  // Retrieves current user after verifying/calling user isLoggedIn  
  public getCurrentUser(): User { 
    const token: string = this.getToken(); 
    const { email, name } = JSON.parse(atob(token.split('.')[1])); 
    return { email, name } as User; 
  } 

  // Returns an observable when the Observable condition is satisfied
  public login(user: User, passwd: string) : void { 
    this.tripDataService.login(user,passwd) 
      .subscribe({ 
        next: (value: any) => { 
          if(value) 
          { 
            console.log(value); 
            this.authResp = value; 
            this.saveToken(this.authResp.token); 
          } 
        }, 
        error: (error: any) => { 
          console.log('Error: ' + error); 
        } 
      }) 
  }  
 
  // Returns an observable when the Observable condition is satisfied
  // NOTE: The API logs a new user in immediately upon registration 
  public register(user: User, passwd: string) : void { 
    this.tripDataService.register(user,passwd) 
      .subscribe({ 
        next: (value: any) => { 
          if(value) 
          { 
            console.log(value); 
            this.authResp = value; 
            this.saveToken(this.authResp.token); 
          } 
        }, 
        error: (error: any) => { 
          console.log('Error: ' + error); 
        } 
      }) 
  }
}
