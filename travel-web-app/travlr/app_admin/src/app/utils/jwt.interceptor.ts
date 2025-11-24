// Interceptor: intercepts data in pipeline to
// perform operations before continuing down pipeline
import { HttpInterceptorFn } from '@angular/common/http';
// Allows changing access and modifying data in a pipeline
import { Injectable,Provider } from '@angular/core'; 
// Client HTML interaction
import { HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http'; 
import { HttpInterceptor, HTTP_INTERCEPTORS } from '@angular/common/http'; 
// RESTful API and http asynchronous interaction
import { Observable } from 'rxjs'; 
// Handles interaction with JWTs
import { AuthenticationService } from '../services/authentication.service';

// @Injectable allows class to function as a provider
@Injectable() 
// HttpInterceptor interface allows interaction in the pipeline
export class JwtInterceptor implements HttpInterceptor { 
  
  // Brings AuthenticationService into class scope
  constructor( 
    private authenticationService: AuthenticationService 
  ) {}

  intercept(request: HttpRequest<any>, next: HttpHandler):  
    Observable<HttpEvent<any>> { 
      // Identify the AuthAPI URL to not intercept
      var isAuthAPI: boolean;
          console.log('Interceptor::URL' + request.url); 
      if(request.url.startsWith('login') || request.url.startsWith('register')) { 
        isAuthAPI = true; 
      } 
      else { 
        isAuthAPI = false; 
      } 

      if(this.authenticationService.isLoggedIn() && !isAuthAPI) { 
        // Grab JWT from AuthenticationService
        let token = this.authenticationService.getToken(); 
        console.log(token); 
        // Clone HTTP request
        const authReq = request.clone({ 
          setHeaders: { 
            Authorization: `Bearer ${token}` 
          } 
        }); 
        // Handle cloned HTTP request
        return next.handle(authReq); 
      } 
      return next.handle(request); 
    }
  }

  export const authInterceptProvider: Provider =  
  { 
    // Unique provider for interceptor module to pull into app.config.ts
    provide: HTTP_INTERCEPTORS,
    useClass: JwtInterceptor,
    multi: true 
  };