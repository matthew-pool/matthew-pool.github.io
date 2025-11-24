import { InjectionToken } from '@angular/core'; 

// BROWSER_STORAGE: token for local storage access
export const BROWSER_STORAGE = new 
    InjectionToken<Storage>('Browser Storage', { 
        providedIn: 'root', 
        factory: () => localStorage 
    });

export class Storage {
}
