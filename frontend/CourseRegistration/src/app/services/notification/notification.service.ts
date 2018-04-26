import { MatSnackBar } from '@angular/material/snack-bar';
import { Injectable } from '@angular/core';

@Injectable()
export class NotificationService {

  constructor(private snackbar: MatSnackBar) { }

  public networkError(resp?) {
    this.snackbar.open('Network Error :(', 'OK', { duration: 3000 });
  }

}
