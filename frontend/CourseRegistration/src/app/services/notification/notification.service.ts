import { MatSnackBar, SimpleSnackBar, MatSnackBarRef } from '@angular/material/snack-bar';
import { Injectable } from '@angular/core';

@Injectable()
export class NotificationService {

  constructor(private snackbar: MatSnackBar) { }

  public showSnackbar(message: string, close: string = 'OK', duration: number = 2000): MatSnackBarRef<SimpleSnackBar> {
    return this.snackbar.open(message, close, { duration });
  }

  public networkError(resp?) {
    this.snackbar.open('Network Error :(', 'OK', { duration: 3000 });
  }

}
