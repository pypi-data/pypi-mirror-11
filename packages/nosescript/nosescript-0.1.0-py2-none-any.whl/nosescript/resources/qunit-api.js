// Micro implementation of QUnit API.
"use_strict";
QUnit.module = function module(name, hooks) {
    QUnit._module(name, hooks);
};

QUnit.test = function(name, test) {
    QUnit._test(name, function() {
        try {
            test(QUnit.assert);
        } catch (e) {
            return {
                name: e.name,
                message: e.message,
                stack: e.stack
            };
        }
    });
};

QUnit.AssertionError = function() {
    var tmp = Error.apply(this, arguments);
    this.name = 'AssertionError';
    this.message = tmp.message;
    this.stack = tmp.stack;
}
QUnit.AssertionError.prototype.toString = function() {
    return this.name + ': ' + this.message;
}

QUnit.assert = {
    ok: function ok(guard, message) {
        if (!guard) {
            message = message || guard + ' evaluation should be true';
            throw new QUnit.AssertionError(message);
        }
    },
    notOk: function notOk(guard, message) {
        this.ok(!guard, message || guard + ' evaluation should be false');
    },
    equal: function equal(expected, actual, message) {
        this.ok(expected == actual, message
                || 'expecting ' + expected + ' == ' + actual)
    },
    notEqual: function notEqual(expected, actual, message) {
        this.ok(expected != actual, message
                || 'expecting ' + expected + ' != ' + actual)
    },
    throws: function throws(block, expected, message) {
        try {
            if (!(expected instanceof Object)) {
                message = expected;
                expected = undefined;
            }
            block();
        } catch (e) {
            if (!expected) return;
            if (expected instanceof RegExp) {
                if (e.toString().match(expected)) return;
                var repr = JSON.stringify(e);
                if (repr.match(expected)) return;
                message = message || repr + ' does not match ' + expected;
                throw new QUnit.AssertionError(message);
            }
            if ((typeof e) === typeof(expected)) {
                return;
            }
            if (expected instanceof Function) {
                if (e instanceof expected) return;
                if (expected(e)) return;
            }
            message = message || e + ' does not match ' + expected;
            throw new QUnit.AssertionError(message);
        }
        message = message || 'Expecting error to be thrown';
        throw new QUnit.AssertionError(message);
    }
};
QUnit.assert.raises = QUnit.assert.throws;
