import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, of, throwError } from 'rxjs';
import { EmailResponse } from '../emailresponse.model';


@Injectable({
  providedIn: 'root'
})

export class EmailService {
  private baseUrl = 'http://127.0.0.1:8000/api/';  // FastAPI Backend URL

  constructor(private http: HttpClient) {}
  uploadFiles(formData: FormData): Observable<EmailResponse[]> {
    return this.http.post<EmailResponse[]>(this.baseUrl + 'process-emails-upload', formData)
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
  
}
