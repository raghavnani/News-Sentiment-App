import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import {Observable, throwError} from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class NewsService {

  private Url = '/api/';  // URL to web api

  constructor(
    private http: HttpClient) { }


getSelectedNews(condition:string, page:number): Observable<any[]> {

  return this.http.get<any[]>(this.Url+'getNewsWithCondition?condition='+condition+'&page='+page.toString())
        .pipe(
          catchError(this.handleError)
        );
}


getSavedNews(): Observable<any[]> {

  return this.http.get<any[]>(this.Url+'getSavedNews/')
        .pipe(
          catchError(this.handleError)
        );
}

updateSavedNews(id, saved): Observable<any> { 

  return this.http.put<any>(this.Url+'updateSavedArticle',{"id": id, 'saved': saved})
        .pipe(
          catchError(this.handleError)
        );
}

// getLatestNews(page:number): Observable<any[]> { 

//   return this.http.get<any[]>(this.Url+'getLatestNews?page='+page.toString())
//         .pipe(
//           catchError(this.handleError)
//         );
// }


getAllUsers(): Observable<any[]> { 

  return this.http.get<any[]>(this.Url+'getAllUsers')
        .pipe(
          catchError(this.handleError)
        );
}


/**
 * Handle Http operation that failed.
 * Let the app continue.
 * @param operation - name of the operation that failed
 * @param result - optional value to return as the observable result
 */
private handleError(error) {
  
  let errorMessage = '';
        if (error.error instanceof ErrorEvent) {
            // client-side error
            errorMessage = `Error: ${error.error.message}`;
        } else {
            // server-side error
            errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
        }
        console.log(errorMessage);
        return throwError(errorMessage);
    }

  }