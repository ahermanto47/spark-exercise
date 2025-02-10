import scala.annotation.tailrec

def randomStringGen(length: Int) = scala.util.Random.alphanumeric.take(length).mkString

// used by #6 and #7
def randomStringFromCharList(length: Int, chars: Seq[Char]): String = {
  val sb = new StringBuilder
  for (i <- 1 to length) {
    val randomNum = util.Random.nextInt(chars.length)
    sb.append(chars(randomNum))
  }
  sb.toString
}

// 1 - a java-esque approach
def randomString(length: Int) = {
  val r = new scala.util.Random
  val sb = new StringBuilder
  for (i <- 1 to length) {
    sb.append(r.nextPrintableChar)
  }
  sb.toString
}

println("1:  " + randomString(10))

def randomStringUsingArray(length: Int): String = {
// 2 - similar to #1, but using an array
  val r = new scala.util.Random
  val a = new Array[Char](length)
  val sb = new StringBuilder
  for (i <- 0 to length-1) {
    a(i) = r.nextPrintableChar
  }
  a.mkString
}

println("2:  " + randomStringUsingArray(10))

// 3 - recursive, but not tail-recursive
def randomStringRecursive(n: Int): List[Char] = {
  n match {
    case 1 => List(util.Random.nextPrintableChar)
    case _ => List(util.Random.nextPrintableChar) ++ randomStringRecursive(n-1)
  }
}

println("3:  " + randomStringRecursive(10).mkString)

// 3b - recursive, but not tail-recursive
def randomStringRecursive2(n: Int): String = {
  n match {
    case 1 => util.Random.nextPrintableChar.toString
    case _ => util.Random.nextPrintableChar.toString ++ randomStringRecursive2(n-1).toString
  }
}

println("3b:  " + randomStringRecursive2(10).mkString)

// 4 - tail recursive, no wrapper
@tailrec
def randomStringTailRecursive(n: Int, list: List[Char]):List[Char] = {
  if (n == 1) util.Random.nextPrintableChar :: list
  else randomStringTailRecursive(n-1, util.Random.nextPrintableChar :: list)
}

// 4 - tail recursive, no wrapper

@tailrec
def randomStringTailRecursive(n: Int, list: List[Char]):List[Char] = {
  if (n == 1) util.Random.nextPrintableChar :: list
  else randomStringTailRecursive(n-1, util.Random.nextPrintableChar :: list)
}

println("4:  " + randomStringTailRecursive(10, Nil).mkString)

// 5 - a wrapper around the tail-recursive approach
def randomStringRecursive2Wrapper(n: Int): String = {
  randomStringTailRecursive(n, Nil).mkString
}

// 6 - random alphanumeric
def randomAlphaNumericString(length: Int): String = {
  val chars = ('a' to 'z') ++ ('A' to 'Z') ++ ('0' to '9')
  randomStringFromCharList(length, chars)
}

println("6:  " + randomAlphaNumericString(10))

// 7 - random alpha
def randomAlpha(length: Int): String = {
  val chars = ('a' to 'z') ++ ('A' to 'Z')
  randomStringFromCharList(length, chars)
}

println("7:  " + randomAlpha(10))

// 8 - random numeric
def randomNumeric(length: Int): String = {
  val chars = ('0' to '9')
  randomStringFromCharList(length, chars)
}

println("8:  " + randomNumeric(10))

def x(length: Int, chars: Seq[Char]): String = {
  val list = List.range(1, length)
  val arr = new Array[Char](length)
  list.foreach{ e => arr(e) = chars(util.Random.nextInt(chars.length)) }
  list.mkString
}

// create a fake list so i can use map (or flatMap)
def x2(length: Int, chars: Seq[Char]): String = {
  val tmpList = List.range(0, length)
  val charList = tmpList.map{ e => chars(util.Random.nextInt(chars.length)) }
  return charList.mkString
}

println("x2: " + x2(10, ('a' to 'z') ++ ('A' to 'Z')))

val df = spark.sparkContext.parallelize(Seq.fill(1000000){(randomStringGen(15),randomAlpha(6), randomAlpha(10), randomNumeric(10))}, 10).toDF("id","firstname", "lastname", "phonenumber")

df.show

df.write.csv("/tmp/test-csv")
