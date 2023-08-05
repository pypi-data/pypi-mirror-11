QUnit.module("Basic unit test");

QUnit.test("basic success", function(assert) {
    assert.equal(2, 1+1);
});

QUnit.test("exceptional case", function(assert) {
    assert.throws(function() {
        var x = null;
        x.y = 42;
    }, /TypeError/);

    assert.throws(function block() {
        assert.throws(function() {
        });
    }, /AssertionError/);

    assert.throws(function() {
        throw "what you expect";
    }, /what you expect/);

    assert.throws(function() {
        throw {message: "what you expect"};
    }, /what you expect/);

    assert.throws(function() {
        assert.throws(function() {
            throw "not the error you were expecting";
        }, /AssertionError/);
    }, QUnit.AssertionError);

    assert.throws(function() {
        assert.throws(function() {
            throw "not the error you were expecting";
        }, QUnit.AssertionError);
    }, QUnit.AssertionError);
});

var FAVORITE_PONY;
QUnit.test("requirement loading", function(assert) {
    FAVORITE_PONY = 'Rainbow Dash';
    require('./reqs/consts.js');
    assert.equal('Fluttershy', FAVORITE_PONY, "require will set global");
    FAVORITE_PONY = 'Rainbow Dash';
    require('./reqs/consts.js');
    assert.equal('Rainbow Dash', FAVORITE_PONY,
                 "require is applied once per context");
});
