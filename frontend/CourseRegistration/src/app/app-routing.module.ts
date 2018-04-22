import { CreateOfferingComponent } from './components/create-offering/create-offering.component';
import { CreateCourseComponent } from './components/create-course/create-course.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserPageComponent } from './components/user-page/user-page.component';
import { CreateStudentComponent } from './components/create-student/create-student.component';

const routes: Routes = [{
  path: 'user',
  component: UserPageComponent,
},
{
  path: 'create-course',
  component: CreateCourseComponent,
},
{
  path: 'create-offering',
  component: CreateOfferingComponent,
},
{
  path: 'create-student',
  component: CreateStudentComponent,
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
