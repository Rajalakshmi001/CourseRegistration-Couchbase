import { CourseTaken } from './course.model';

export interface User {
    username?: String;
    name: String;
    type: 'stud' | 'prof';
    courses: CourseTaken[];
}
