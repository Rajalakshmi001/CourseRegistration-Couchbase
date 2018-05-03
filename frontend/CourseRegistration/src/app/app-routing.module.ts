import { CreateOfferingComponent } from './pages/create-offering/create-offering.component';
import { CreateCourseComponent } from './pages/create-course/create-course.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CreateUserComponent } from './pages/create-student/create-student.component';
import { RegisterComponent } from './pages/register/register.component';
import { LookupComponent } from './pages/lookup/lookup.component';
import { HomeComponent } from './pages/home/home.component';
import { SearchComponent } from './pages/search/search.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  }, {
    path: 'create-course',
    component: CreateCourseComponent
  }, {
    path: 'create-offering',
    component: CreateOfferingComponent
  }, {
    path: 'create-user',
    component: CreateUserComponent
  }, {
    path: 'register',
    component: RegisterComponent
  }, {
    path: 'lookup',
    component: LookupComponent
  }, {
    path: 'search',
    component: SearchComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
exports: [RouterModule]
})
export class AppRoutingModule { }
