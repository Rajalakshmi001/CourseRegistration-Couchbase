import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { UserPageComponent } from './components/user-page/user-page.component';
import { CreateCourseComponent } from './components/create-course/create-course.component';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { HttpModule, Http } from '@angular/http';
import { CreateOfferingComponent } from './components/create-offering/create-offering.component';
import { MatSelectModule } from '@angular/material/select';
import { CreateUserComponent } from './components/create-student/create-student.component';

@NgModule({
  declarations: [
    AppComponent,
    UserPageComponent,
    CreateCourseComponent,
    CreateOfferingComponent,
    CreateUserComponent,
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
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
