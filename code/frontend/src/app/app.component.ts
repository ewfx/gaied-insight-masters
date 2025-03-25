import { Component } from '@angular/core';
import { EmailService } from './service/email.service';
import { EmailResponse } from './emailresponse.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'frontend';
  isProcessing = false;
  emailResults: EmailResponse[] = [];

  constructor(private emailService: EmailService) {}

  onFilesProcessed(formData: FormData) {
    this.isProcessing = true;
    this.emailService.uploadFiles(formData).subscribe({
      next: (response: EmailResponse[]) => {
        this.emailResults = response;
        this.isProcessing = false;
      },
      error: (error) => {
        console.error('Error processing files:', error);
        console.log('Error object: ', error); //add this.
        this.emailResults = [];
      },
    });
  }

  processDirectoryEmails() {
    this.isProcessing = true;
    this.emailService.processEmailDirectory().subscribe({
      next: (response: EmailResponse[]) => {
        this.emailResults = response;
        this.isProcessing = false;
      },
      error: (error) => {
        console.error('Error processing directory emails:', error);
        console.log('Error object: ', error);
        this.emailResults = [];
        this.isProcessing = false;
      },
    });
  }
}
