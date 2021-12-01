import Dependencies._

ThisBuild / scalaVersion     := "2.13.3"
ThisBuild / version          := "0.1.0"
ThisBuild / organization     := "org.scala.thundzz"

lazy val root = (project in file("."))
  .settings(
    name := "advent-of-code-2021",
    scalacOptions ++= Seq("-deprecation", "-feature"),
    libraryDependencies += scalaTest % Test
  )
