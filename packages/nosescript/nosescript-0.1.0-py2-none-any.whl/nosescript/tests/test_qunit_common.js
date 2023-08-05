// shamelessly ripped tests from QUnit documentation
QUnit.test( "ok test", function( assert ) {
  assert.ok( true, "true succeeds" );
  assert.ok( "non-empty", "non-empty string succeeds" );

  assert.notOk( false, "false fails" );
  assert.notOk( 0, "0 fails" );
  assert.notOk( NaN, "NaN fails" );
  assert.notOk( "", "empty string fails" );
  assert.notOk( null, "null fails" );
  assert.notOk( undefined, "undefined fails" );
});

QUnit.test( "equal test", function( assert ) {
  assert.equal( 0, 0, "Zero, Zero; equal succeeds" );
  assert.equal( "", 0, "Empty, Zero; equal succeeds" );
  assert.equal( "", "", "Empty, Empty; equal succeeds" );

  assert.notEqual( "three", 3, "Three, 3; equal fails" );
  assert.notEqual( null, false, "null, false; equal fails" );
});

