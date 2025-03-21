import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

interface EmailResponse {
  email: string;
  status: string;
  message: string;
}

@Injectable({
  providedIn: 'root'
})

export class EmailService {
  //private baseUrl = 'http://localhost:8000';  // FastAPI Backend URL
    private apiUrl = 'http://127.0.0.1:8000/upload/'

  constructor(private http: HttpClient) {}

  /** Upload multiple email files */
  // uploadFiles(files: File[]): Observable<any> {
  //   const formData = new FormData();
  //   files.forEach(file => formData.append('files', file));

  //   return this.http.post(`${this.baseUrl}/upload-email`, formData);
  // }
  uploadFiles(formData: FormData): Observable<EmailResponse[]> {
    return this.http.post<EmailResponse[]>(this.apiUrl, formData);
  }
  uploadFiles2(formData: FormData): Observable<EmailResponse[]> {

    const dummyData: EmailResponse[] = [
      { email: 'test1@example.com', status: 'Success', message: 'Email processed successfully.' },
      { email: 'invalid@example', status: 'Failed', message: 'Invalid email format.' },
      { email: 'test2@example.com', status: 'Success', message: 'Email processed successfully.' },
      { email: 'test3@example.com', status: 'Success', message: 'Email processed successfully.' },
      { email: 'test4@example.com', status: 'Failed', message: 'Some error processing email' },
    ];
    // Return dummy data instead of API call.
    return of(dummyData);
    // return this.http.post<EmailResponse[]>(this.apiUrl, formData); // Uncomment for real API call
  }
  /** Process emails for classification */
  // processEmails(directory: string): Observable<any> {
  //   return this.http.get(`${this.baseUrl}/process-emails?directory=${directory}`);
  // }

  // /** Get processed email results */
  // getEmailResults(): Observable<any> {
  //   return this.http.get(`${this.baseUrl}/get-email-results`);
  // }
}
