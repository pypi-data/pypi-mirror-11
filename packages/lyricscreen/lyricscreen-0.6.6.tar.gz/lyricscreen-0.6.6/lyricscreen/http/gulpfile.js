var gulp = require('gulp');
var sourcemaps = require('gulp-sourcemaps');
var livereload = require('gulp-livereload');
var sass = require('gulp-sass');
var rev = require('gulp-rev');
var concat = require('gulp-concat');
var gulpif = require('gulp-if');
var _ = require('underscore');
var del = require('del');

/*
 |----------------------------------------------------------------
 | Build lytedev
 |----------------------------------------------------------------
 |
 | Build the lytedev resources, dawg.
 |
 */

// TODO: Scripts task

gulp.task('styles', function(options) {

    var defaults = {
        outputStyle: 'nested'
    };

    src = "sass/*.scss";
    // var s = 0;
    // del("css/*.css", { force: true }, function() {
        var stream = gulp.src(src)
            .pipe(sourcemaps.init())
                .pipe(sass(_.extend(defaults, options)))
            .pipe(sourcemaps.write('./maps'))
            .pipe(gulp.dest("css"))
    // });

    return stream;

});

gulp.task('build-styles', ['styles'], function() {

    del("css/all.css", { force: true }, function() {
        gulp.src([
                './bower_components/normalize.css/normalize.css',
                "css/*.css"
            ])
            .pipe(concat('all.css'))
            .pipe(gulp.dest("css"));
    });

});

gulp.task('build-scripts', [], function() {

    // TODO: Build scripts

});

gulp.task('build', ['build-styles'], function() {

    var buildDir = 'build';
    var cssBuildDir = "css/*.css"
    var jsBuildDir = "js/*.js"

    del(buildDir, { force: true }, function() {
        gulp.src([cssBuildDir, jsBuildDir])
            .pipe(gulp.dest(buildDir))
            // .pipe(rev())
            .pipe(gulp.dest(buildDir))
            // .pipe(rev.manifest())
            .pipe(gulp.dest(buildDir))
    });

});

gulp.task('default', ['build'], function() {

});

gulp.task('livereload', [], function() {

    livereload.changed();

});

gulp.task('reload-styles', ['build-styles'], function() {

    livereload.changed();

});

gulp.task('reload-scripts', ['build-scripts'], function() {

    livereload.changed();

});

gulp.task('watch', ['default'], function() {

    livereload.listen();
    
    gulp.watch("sass/*.scss", ['reload-styles']);
    gulp.watch("js/*.js", ['reload-scripts']);
    gulp.watch("*.html", ['livereload']);

});

