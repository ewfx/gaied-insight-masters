import { Component } from '@angular/core';
import { EmailService } from './service/email.service';

interface EmailResponse {
  email: string;
  status: string;
  message: string;
}
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'frontend';
  isProcessing = false;
  emailResults: EmailResponse[] = [];

  constructor(private emailService: EmailService) {}

  onFilesProcessed(formData: FormData) {
    this.emailService.uploadFiles2(formData).subscribe({
      next: (response: EmailResponse[]) => {
        this.emailResults = response;
      },
      error: (error) => {
        console.error('Error processing files:', error);
        this.emailResults = [];
      },
    });
  }
}
