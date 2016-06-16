import autoprefixer from 'autoprefixer';
import gulp from 'gulp';
import postcss from 'gulp-postcss';
import sass from 'gulp-sass';

gulp.task('material-icons.font', () => {
  return gulp.src('./node_modules/material-design-icons/iconfont/*')
    .pipe(gulp.dest('./django_materialize/static/django_materialize/fonts/material-design-icons/'));
});


gulp.task('roboto.font', () => {
  return gulp.src('./node_modules/materialize-css/fonts/roboto/*')
    .pipe(gulp.dest('./django_materialize/static/django_materialize/fonts/roboto/'));
});



gulp.task('materialize.js', () => {
  return gulp.src('./node_modules/materialize-css/dist/js/materialize.js')
    .pipe(gulp.dest('./django_materialize/static/django_materialize/js/'));
});


gulp.task('materialize.css', () => {
  return gulp.src('./django_materialize/static/django_materialize/sass/*.scss')
    .pipe(sass({
      includePaths: './node_modules/'
    }).on(
      'error', sass.logError
    ))
    .pipe(postcss([
      autoprefixer({
        browsers: [
          'Chrome >= 50',
          'Firefox >= 46',
          'Explorer >= 11',
          'Safari >= 9',
          'ChromeAndroid >= 50',
          'FirefoxAndroid >= 46',
        ]
      })
    ]))
    .pipe(gulp.dest(
      './django_materialize/static/django_materialize/css/'
    ));
});


gulp.task("default", [
  "materialize.js",
  "materialize.css",
  "roboto.font",
  "material-icons.font"
]);
