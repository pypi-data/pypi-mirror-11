package org.python.types;

public class Int extends org.python.types.Object {
    public long value;

    /**
     * Return the python name for this class.
     */
    public java.lang.String getPythonName() {
        return "int";
    }

    /**
     * A utility method to update the internal value of this object.
     *
     * Used by __i*__ operations to do an in-place operation.
     * obj must be of type org.python.types.Int
     */
    void setValue(org.python.Object obj) {
        this.value = ((org.python.types.Int) obj).value;
    }

    public Int(byte value) {
        this.value = (long) value;
    }

    public Int(short value) {
        this.value = (long) value;
    }

    public Int(int value) {
        this.value = (long) value;
    }

    public Int(long value) {
        this.value = value;
    }

    // public org.python.Object __new__() {
    //     throw new org.python.exceptions.NotImplementedError("int.__new__() has not been implemented");
    // }

    // public org.python.Object __init__() {
    //     throw new org.python.exceptions.NotImplementedError("int.__init__() has not been implemented");
    // }

    public org.python.types.Str __repr__() {
        return new org.python.types.Str(java.lang.Long.toString(this.value));
    }

    public org.python.types.Str __format__() {
        throw new org.python.exceptions.NotImplementedError("int.__format__() has not been implemented");
    }

    public org.python.Object __lt__(org.python.Object other) {
        if (other instanceof org.python.types.Int) {
            return new org.python.types.Bool(this.value < ((org.python.types.Int) other).value);
        } else if (other instanceof Float) {
            return new org.python.types.Bool(((double) this.value) < ((org.python.types.Float) other).value);
        }
        throw new org.python.exceptions.TypeError("unorderable types: int() < " + other.getClass().getName() + "()");
    }

    public org.python.Object __le__(org.python.Object other) {
        if (other instanceof org.python.types.Int) {
            return new org.python.types.Bool(this.value < ((org.python.types.Int) other).value);
        } else if (other instanceof Float) {
            return new org.python.types.Bool(((double) this.value) <= ((org.python.types.Float) other).value);
        }
        throw new org.python.exceptions.TypeError("unorderable types: int() <= " + other.getClass().getName() + "()");
    }

    public org.python.Object __eq__(org.python.Object other) {
        if (other instanceof org.python.types.Int) {
            return new org.python.types.Bool(this.value < ((org.python.types.Int) other).value);
        } else if (other instanceof Float) {
            return new org.python.types.Bool(((double) this.value) == ((org.python.types.Float) other).value);
        }
        throw new org.python.exceptions.TypeError("unorderable types: int() == " + other.getClass().getName() + "()");
    }

    public org.python.Object __ne__(org.python.Object other) {
        if (other instanceof org.python.types.Int) {
            return new org.python.types.Bool(this.value < ((org.python.types.Int) other).value);
        } else if (other instanceof Float) {
            return new org.python.types.Bool(((double) this.value) != ((org.python.types.Float) other).value);
        }
        throw new org.python.exceptions.TypeError("unorderable types: int() != " + other.getClass().getName() + "()");
    }

    public org.python.Object __gt__(org.python.Object other) {
        if (other instanceof org.python.types.Int) {
            return new org.python.types.Bool(this.value < ((org.python.types.Int) other).value);
        } else if (other instanceof Float) {
            return new org.python.types.Bool(((double) this.value) > ((org.python.types.Float) other).value);
        }
        throw new org.python.exceptions.TypeError("unorderable types: int() > " + other.getClass().getName() + "()");
    }

    public org.python.Object __ge__(org.python.Object other) {
        if (other instanceof org.python.types.Int) {
            return new org.python.types.Bool(this.value < ((org.python.types.Int) other).value);
        } else if (other instanceof Float) {
            return new org.python.types.Bool(((double) this.value) >= ((org.python.types.Float) other).value);
        }
        throw new org.python.exceptions.TypeError("unorderable types: int() >= " + other.getClass().getName() + "()");
    }

    public org.python.types.Bool __bool__() {
        throw new org.python.exceptions.NotImplementedError("int.__bool__() has not been implemented");
    }

    public org.python.Object __getattribute__(java.lang.String name) {
        throw new org.python.exceptions.NotImplementedError("int.__getattribute__() has not been implemented");
    }

    public void __setattr__(java.lang.String name, org.python.Object value) {
        throw new org.python.exceptions.NotImplementedError("int.__setattr__() has not been implemented");
    }

    public void __delattr__(java.lang.String name) {
        throw new org.python.exceptions.NotImplementedError("int.__delattr__() has not been implemented");
    }

    public org.python.types.List __dir__() {
        throw new org.python.exceptions.NotImplementedError("int.__dir__() has not been implemented");
    }

    public org.python.Object __add__(org.python.Object other) {
        if (other instanceof org.python.types.Int) {
            return new org.python.types.Int(this.value + ((org.python.types.Int) other).value);
        } else if (other instanceof org.python.types.Float) {
            return new org.python.types.Float(((double) this.value) + ((org.python.types.Float) other).value);
        }
        throw new org.python.exceptions.TypeError("unsupported operand type(s) for +: 'int' and '" + other.getClass().getName() + "'");
    }

    public org.python.Object __sub__(org.python.Object other) {
        if (other instanceof org.python.types.Str) {
            return other.__sub__(this);
        } else if (other instanceof org.python.types.Int) {
            return new org.python.types.Int(this.value - ((org.python.types.Int) other).value);
        } else if (other instanceof org.python.types.Float) {
            return new org.python.types.Float(((double) this.value) - ((org.python.types.Float) other).value);
        }
        throw new org.python.exceptions.TypeError("unsupported operand type(s) for -: 'int' and '" + other.getClass().getName() + "'");
    }

    public org.python.Object __mul__(org.python.Object other) {
        if (other instanceof org.python.types.Str) {
            return other.__mul__(this);
        } else if (other instanceof org.python.types.Int) {
            return new org.python.types.Int(this.value * ((org.python.types.Int) other).value);
        } else if (other instanceof org.python.types.Float) {
            return new org.python.types.Float(((double) this.value) * ((org.python.types.Float) other).value);
        } else if (other instanceof org.python.types.List) {
            return other.__mul__(this);
        } else if (other instanceof org.python.types.Tuple) {
            return other.__mul__(this);
        }
        throw new org.python.exceptions.TypeError("unsupported operand type(s) for *: 'int' and '" + other.getClass().getName() + "'");
    }

    public org.python.Object __truediv__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__truediv__() has not been implemented");
    }

    public org.python.Object __floordiv__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__floordiv__() has not been implemented");
    }

    public org.python.Object __mod__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__mod__() has not been implemented");
    }

    public org.python.Object __divmod__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__divmod__() has not been implemented");
    }

    public org.python.Object __pow__(org.python.Object other) {
        if (other instanceof org.python.types.Int) {
            long result = this.value;
            for (long count = 1; count < ((org.python.types.Int) other).value; count++) {
                result *= this.value;
            }
            return new org.python.types.Int(result);
        } else if (other instanceof org.python.types.Float) {
            return new org.python.types.Float(java.lang.Math.pow((double) this.value, ((org.python.types.Float) other).value));
        }
        throw new org.python.exceptions.TypeError("unsupported operand type(s) for ** or pow(): 'int' and '" + other.getClass().getName() + "'");
    }

    public org.python.Object __lshift__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__lshift__() has not been implemented");
    }

    public org.python.Object __rshift__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rshift__() has not been implemented");
    }

    public org.python.Object __and__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__and__() has not been implemented");
    }

    public org.python.Object __xor__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__xor__() has not been implemented");
    }

    public org.python.Object __or__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__or__() has not been implemented");
    }

    public org.python.Object __radd__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__radd__() has not been implemented");
    }

    public org.python.Object __rsub__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rsub__() has not been implemented");
    }

    public org.python.Object __rmul__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rmul__() has not been implemented");
    }

    public org.python.Object __rtruediv__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rtruediv__() has not been implemented");
    }

    public org.python.Object __rfloordiv__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rfloordiv__() has not been implemented");
    }

    public org.python.Object __rmod__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rmod__() has not been implemented");
    }

    public org.python.Object __rdivmod__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rdivmod__() has not been implemented");
    }

    public org.python.Object __rpow__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rpow__() has not been implemented");
    }

    public org.python.Object __rlshift__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rlshift__() has not been implemented");
    }

    public org.python.Object __rrshift__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rrshift__() has not been implemented");
    }

    public org.python.Object __rand__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rand__() has not been implemented");
    }

    public org.python.Object __rxor__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__rxor__() has not been implemented");
    }

    public org.python.Object __ror__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("int.__ror__() has not been implemented");
    }

    public org.python.Object __neg__() {
        throw new org.python.exceptions.NotImplementedError("int.__neg__() has not been implemented");
    }

    public org.python.Object __pos__() {
        throw new org.python.exceptions.NotImplementedError("int.__pos__() has not been implemented");
    }

    public org.python.Object __abs__() {
        if (this.value < 0) {
            return new org.python.types.Int(-this.value);
        } else {
            return new org.python.types.Int(this.value);
        }
    }

    public org.python.Object __invert__() {
        throw new org.python.exceptions.NotImplementedError("int.__invert__() has not been implemented");
    }

    public org.python.types.Int __int__() {
        return new org.python.types.Int(this.value);
    }

    public org.python.types.Float __float__() {
        return new org.python.types.Float((float) this.value);
    }

    public org.python.Object __round__() {
        throw new org.python.exceptions.NotImplementedError("int.__round__() has not been implemented");
    }


}