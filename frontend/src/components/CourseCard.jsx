import { BookOpen } from "lucide-react";

export default function CourseCard({ course }) {
  return (
    <article className="course-card">
      <div className="course-icon">
        <BookOpen size={18} />
      </div>

      <div>
        <h4>{course.name}</h4>
        <p>{course.provider}</p>
        <span>{course.level}</span>
      </div>
    </article>
  );
}
