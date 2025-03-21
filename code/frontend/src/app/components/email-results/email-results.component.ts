import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { EmailService } from '../../service/email.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';

interface EmailResponse {
  email: string;
  status: string;
  message: string;
}


@Component({
  selector: 'app-email-results',
  templateUrl: './email-results.component.html',
  styleUrls: ['./email-results.component.scss'],
  standalone: false
})
export class EmailResultsComponent implements OnInit {
  emails: any[] = [];
  isLoading = true;
  hoveredRow: any;

  @Input() emailResponses: EmailResponse[] = [];
  displayedColumns: string[] = ['email', 'status', 'message'];
  dataSource = new MatTableDataSource<EmailResponse>(this.emailResponses);

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(private emailService: EmailService) {}

  ngOnInit() {  
  }
  ngOnChanges() {
    this.dataSource.data = this.emailResponses;
    this.dataSource.paginator = this.paginator;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
  
  onRowHover(row: any) {
    this.hoveredRow = row;
  }

  onRowLeave() {
    this.hoveredRow = null;
  }
  // this.emailService.getEmailResults().subscribe({
  //   next: (data) => {
  //     this.emails = data;
  //     this.isLoading = false;
  //   },
  //   error: () => {
  //     console.error('Failed to fetch email data');
  //     this.isLoading = false;
  //   }
  // });
}
