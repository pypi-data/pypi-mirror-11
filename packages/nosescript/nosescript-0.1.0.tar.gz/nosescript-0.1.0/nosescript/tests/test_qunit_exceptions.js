// shamelessly ripped tests from QUnit documentation
QUnit.test( "throws", function( assert ) {

  function CustomError( message ) {
    this.message = message;
  }

  CustomError.prototype.toString = function() {
    return this.message;
  };

  assert.throws(
    function() {
      throw "error"
    },
    "throws with just a message, not using the 'expected' argument"
  );

  assert.throws(
    function() {
      throw new CustomError("some error description");
    },
    /description/,
    "raised error message contains 'description'"
  );

  assert.throws(
    function() {
      throw new CustomError();
    },
    CustomError,
    "raised error is an instance of CustomError"
  );

  assert.throws(
    function() {
      throw new CustomError("some error description");
    },
    new CustomError("some error description"),
    "raised error instance matches the CustomError instance"
  );

  assert.throws(
    function() {
      throw new CustomError("some error description");
    },
    function( err ) {
      return err.toString() === "some error description";
    },
    "raised error instance satisfies the callback function"
  );
});
