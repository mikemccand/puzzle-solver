import scala.math.{Pi, cos, sin}

case class Point(val x: Int, val y: Int, val z: Int) {
  override def toString() = {
    s"[$x,$y,$z]"
  }

  def valid = {
    val bX = 3
    val bY = 3
    val bZ = 3
    x >= 0 && x <= bX && y >= 0 && y <= bY && z >= 0 && z <= bZ
  }

  def move(dx: Int, dy: Int, dz: Int) = Point(x + dx, y + dy, z + dz)

  def rotate(axis: Point, angle: Int): Point = {
    val sinA = math.round(math.sin(math.toRadians(angle))).toInt
    val cosA = math.round(math.cos(math.toRadians(angle))).toInt
    axis match {
      case Point(1, 0, 0) =>
        // Rotate around the X axis
        Point(
          x,
          y * cosA - z * sinA,
          y * sinA + z * cosA
        )
      case Point(0, 1, 0) =>
        // Rotate around the Y axis
        Point(
          x * cosA - z * sinA,
          y,
          x * sinA + z * cosA
        )
      case Point(0, 0, 1) =>
        // Rotate around the Z axis
        Point(
          x * cosA + y * sinA,
         -x * sinA + y * cosA,
          z
        )
      case _ =>
        throw new IllegalArgumentException("Invalid axis")
    }
  }
}

case class Piece(val id: Int, val points: Set[Point]) {
  def ps = this.points
  override def toString() = {
    s"[$id] ${points.size} pts\n"
  }

  def move(dx: Int, dy: Int, dz: Int) = {
    Piece(id, points.map { p => p.move(dx, dy, dz) })
  }

  def rotate(axis: Point, angle: Int) = {
    Piece(id, points.map{ p => p.rotate(axis, angle) })
  }

  def valid = {
    points.forall { p => p.valid }
  }
  
  def variations = {
    val Rx = Point(1, 0, 0)
    val Ry = Point(0, 1, 0)
    val Rz = Point(0, 0, 1)
    val pieces = for {
      x <- -7 to 7
      y <- -7 to 7
      z <- -7 to 7
      angleX <- List(0, 90, 180, 270)
      angleY <- List(0, 90, 180, 270)
      angleZ <- List(0, 90, 180, 270)
    } yield rotate(Rx, angleX).rotate(Ry, angleY).rotate(Rz, angleZ).move(x, y, z)
    pieces.filter{ p => p.valid }.toSet.toArray
  }
}

object Piece {
  def apply(id: Int, points: List[(Int, Int, Int)]) = {
    new Piece(id, points.map { case (x, y, z) => new Point(x, y, z) }.toSet)
  }
}

def solve(pieces: Array[Array[Piece]]): (Set[Point], List[Int]) = {
  var solutions = pieces(0).zipWithIndex.map(p => (p._1.points, List(p._2)))
  for (k <- 1 to (pieces.size - 1)) {
    println(s"$k: ${solutions.size}")
    var newSol = Array[(Set[Point], List[Int])]()
    for (prev <- solutions) {
      val state: Set[Point] = prev._1
      val l: List[Int] = prev._2
      for ((c, v) <- pieces(k).zipWithIndex) {
        val fit = state.union(c.points)
        if (fit.size == (state.size + c.points.size)) {
          val newFit = (fit, v :: l)
          newSol = newSol.appended(newFit)
        }
      }
    }
    if(newSol.size == 0) {
      println("Stuck")
    }
    solutions = newSol
  }

  return solutions(0)
}

var pieces = List(
  Piece(1, List((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 1))),
  Piece(2, List((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1))),
  Piece(3, List((0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (2, 0, 1))),
  Piece(
    4,
    List((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 1, 1), (2, 1, 1), (2, 2, 1))
  ),
  Piece(
    5,
    List((0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (1, 1, 0), (2, 0, 1))
  ),
  Piece(
    6,
    List(
      (0, 0, 0),
      (1, 0, 0),
      (2, 0, 0),
      (3, 0, 0),
      (0, 1, 0),
      (3, 1, 0),
      (3, 1, 1),
      (3, 1, 2)
    )
  ),
  Piece(
    7,
    List(
      (0, 0, 0),
      (1, 0, 0),
      (2, 0, 0),
      (0, 0, 1),
      (2, 0, 1),
      (2, 0, 2),
      (2, 1, 0),
      (2, 1, 1)
    )
  ),
  Piece(
    8,
    List(
      (0, 0, 0),
      (1, 0, 0),
      (2, 0, 0),
      (1, 0, 1),
      (0, 1, 0),
      (1, 1, 0),
      (0, 1, 1),
      (1, 1, 1),
      (0, 1, 2)
    )
  ),
  Piece(
    9,
    List(
      (0, 0, 0),
      (3, 0, 0),
      (0, 0, 1),
      (3, 0, 1),
      (0, 0, 2),
      (0, 1, 0),
      (1, 1, 0),
      (2, 1, 0),
      (3, 1, 0),
      (1, 2, 0),
      (1, 3, 0),
      (1, 3, 1),
      (1, 3, 2)
    )
  )
)

object Main {
    def main(args: Array[String]): Unit = {
        val vars = pieces.reverse.map { p => p.variations }.toArray

        val sol = solve(vars)._2.reverse

        println("\nSolution:")
        sol.zipWithIndex.foreach {(v,p) =>
          println("np.array(["+vars(p)(v).ps.toList.mkString(", ")+"]),")
        }
    }
}
