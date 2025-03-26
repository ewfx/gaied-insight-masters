import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, of, throwError } from 'rxjs';
import { EmailResponse } from '../emailresponse.model';
import { environment } from '../../environment/environment';


@Injectable({
  providedIn: 'root'
})

export class EmailService {
  // private baseUrl = 'http://127.0.0.1:8000/api/';  // FastAPI Backend URL
  private baseUrl = environment.apiBaseUrl;
  constructor(private http: HttpClient) {}
  uploadFiles(formData: FormData): Observable<EmailResponse[]> {
    return this.http.post<EmailResponse[]>(this.baseUrl + 'process-emails-upload/', formData)
    .pipe(
      catchError((error) => {
        console.error('Error uploading files:', error);
        return throwError('An error occurred during file upload.'); // Or handle the error as needed
      })
  );
  }

  processEmailDirectory(): Observable<EmailResponse[]> {
    return this.http.post<EmailResponse[]>(this.baseUrl + 'process-email-directory/', {}); // Empty body as the path is on the server
  }

  uploadRuleFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name); // 'ruleFile' is the field name your backend expects

    return this.http.post(`${this.baseUrl}upload-priority-rules/`, formData)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: any): Observable<any> {
    console.error('File upload error:', error);
    let errorMessage = 'An error occurred during file upload.';
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      if (error.status) {
        errorMessage = `Error Code: ${error.status}, Message: ${error.error?.message || error.message || 'Unknown server error'}`;
      }
    }
    return throwError(() => new Error(errorMessage));
  }
  
}
