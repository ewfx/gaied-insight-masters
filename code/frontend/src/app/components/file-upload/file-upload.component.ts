import { Component, EventEmitter, Output } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EmailService } from '../../service/email.service';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss'],
  standalone: false
})
export class FileUploadComponent {
  selectedFiles: File[] = [];
  isUploading = false;
  progress = 0;

  files: File[] = [];
  processing: boolean = false;
  processComplete: boolean = false;
  @Output() filesProcessed = new EventEmitter<FormData>();

  constructor(private emailService: EmailService, private snackBar: MatSnackBar) {}

  // onFileSelected(event: any) {
  //   this.selectedFiles = Array.from(event.target.files);
  // }

  // uploadFiles() {
  //   if (this.selectedFiles.length === 0) {
  //     this.snackBar.open('Please select files first!', 'Close', { duration: 3000 });
  //     return;
  //   }

  //   this.isUploading = true;
  //   this.progress = 0;

  //   this.emailService.uploadFiles(this.selectedFiles).subscribe({
  //     next: () => {
  //       this.isUploading = false;
  //       this.progress = 100;
  //       this.snackBar.open('Files uploaded successfully!', 'Close', { duration: 3000 });
  //     },
  //     error: () => {
  //       this.isUploading = false;
  //       this.snackBar.open('Error uploading files!', 'Close', { duration: 3000 });
  //     }
  //   });
  // }

  handleDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  handleDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    const droppedFiles = event.dataTransfer?.files;
    if (droppedFiles) {
      this.files = Array.from(droppedFiles);
    }
  }

  handleFileInput(event: any) {
    this.files = Array.from(event.target.files);
  }

  processFiles() {
    this.processing = true;
    this.processComplete = false;

    const formData = new FormData();
    this.files.forEach(file => {
      formData.append('files', file, file.name);
    });
    this.filesProcessed.emit(formData);
  }
}
