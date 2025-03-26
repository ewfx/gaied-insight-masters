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

  selectedRulesFile: File | null = null;
  uploadMessage: string = '';
  uploadError: string = '';

  constructor(private emailService: EmailService) {}

  onFilesProcessed(formData: FormData) {
    this.isProcessing = true;
    this.emailService.uploadFiles(formData).subscribe({
      next: (response: EmailResponse[]) => {
        //this.emailResults = response;
        this.emailResults = response.map(item => {
          if (item.all_extracted_numbers && Array.isArray(item.all_extracted_numbers)) {
            const manipulatedArray: string[] = item.all_extracted_numbers.map(obj => {
              const keys = Object.keys(obj);
              // Assuming each object has one key-value pair
              if (keys.length > 0) {
                return `${keys[0]}: ${obj[keys[0]]}`;
              }
              return '';
            });
            // Join the strings into a single comma-separated string
            item.all_extracted_numbers = manipulatedArray.join(', ');
          }
          return item;
        });
        
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
       
        //this.emailResults = response;
        this.emailResults = response.map(item => {
          if (item.all_extracted_numbers && Array.isArray(item.all_extracted_numbers)) {
            const manipulatedArray: string[] = item.all_extracted_numbers.map(obj => {
              const keys = Object.keys(obj);
              // Assuming each object has one key-value pair
              if (keys.length > 0) {
                return `${keys[0]}: ${obj[keys[0]]}`;
              }
              return '';
            });
            // Join the strings into a single comma-separated string
            item.all_extracted_numbers = manipulatedArray.join(', ');
          }
          return item;
        });
        
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

  onFileSelected(event: any): void {
    this.selectedRulesFile = event.target.files[0];
    this.uploadMessage = '';
    this.uploadError = '';
  }
  uploadRuleFile(): void {
    this.isProcessing = true;
    if (this.selectedRulesFile) {
      this.uploadMessage = 'Uploading file...';
      this.uploadError = '';

      this.emailService.uploadRuleFile(this.selectedRulesFile).subscribe({
        next: (response) => {
          this.uploadMessage = 'File uploaded successfully!';
          this.isProcessing = false;
        },
        error: (error) => {
          this.uploadError = error.message;
          this.uploadMessage = '';
          console.error('File upload failed:', error);
        },
      });
    } else {
      this.uploadMessage = 'Please select a file to upload.';
    }
  }
}
