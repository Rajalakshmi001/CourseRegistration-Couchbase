import { CourseTaken } from './course.model';

export interface User {
    id?: String;
    name: String;
    courses: CourseTaken[];
}
