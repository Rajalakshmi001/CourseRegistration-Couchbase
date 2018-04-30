import { DatabaseService } from './services/database/database.service';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { CreateCourseComponent } from './pages/create-course/create-course.component';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { HttpModule, Http } from '@angular/http';
import { CreateOfferingComponent } from './pages/create-offering/create-offering.component';
import { MatSelectModule } from '@angular/material/select';
import { CreateUserComponent } from './pages/create-student/create-student.component';
import { RegisterComponent, FilterPipe } from './pages/register/register.component';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { LookupComponent } from './pages/lookup/lookup.component';
import { MatTableModule } from '@angular/material/table';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { DeviceService } from './services/device/device.service';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { NotificationService } from './services/notification/notification.service';
import { HomeComponent } from './pages/home/home.component';
import { InfoMessageComponent } from './components/info-message/info-message.component';

@NgModule({
  declarations: [
    AppComponent,
    CreateCourseComponent,
    CreateOfferingComponent,
    CreateUserComponent,
    RegisterComponent,
    FilterPipe,
    LookupComponent,
    HomeComponent,
    InfoMessageComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatCardModule,
    MatInputModule,
    ReactiveFormsModule,
    MatButtonModule,
    HttpModule,
    MatSelectModule,
    MatAutocompleteModule,
    MatTableModule,
    MatSidenavModule,
    MatListModule,
    MatIconModule,
    MatSnackBarModule,
  ],
  providers: [DeviceService, NotificationService, DatabaseService],
  bootstrap: [AppComponent]
})
export class AppModule { }
