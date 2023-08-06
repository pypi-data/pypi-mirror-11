package org.python.types;

public class Float extends org.python.types.Object {
    public double value;

    /**
     * Return the python name for this class.
     */
    public java.lang.String getPythonName() {
        return "float";
    }

    /**
     * A utility method to update the internal value of this object.
     *
     * Used by __i*__ operations to do an in-place operation.
     * obj must be of type org.python.types.Float
     */
    void setValue(org.python.Object obj) {
        this.value = ((org.python.types.Float) obj).value;
    }

    public Float(float value) {
        super();
        this.value = (double) value;
    }

    public Float(double value) {
        super();
        this.value = value;
    }

    // public org.python.Object __new__() {
    //     throw new org.python.exceptions.NotImplementedError("float.__new__() has not been implemented.");
    // }

    // public org.python.Object __init__() {
    //     throw new org.python.exceptions.NotImplementedError("float.__init__() has not been implemented.");
    // }

    public org.python.types.Str __repr__() {
        return new org.python.types.Str(java.lang.Double.toString(this.value));
    }

    public org.python.types.Str __format__() {
        throw new org.python.exceptions.NotImplementedError("float.__format__() has not been implemented.");
    }

    public org.python.Object __lt__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__lt__() has not been implemented.");
    }

    public org.python.Object __le__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__le__() has not been implemented.");
    }

    public org.python.Object __eq__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__eq__() has not been implemented.");
    }

    public org.python.Object __ne__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__ne__() has not been implemented.");
    }

    public org.python.Object __gt__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__gt__() has not been implemented.");
    }

    public org.python.Object __ge__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__ge__() has not been implemented.");
    }

    public org.python.types.Bool __bool__() {
        throw new org.python.exceptions.NotImplementedError("float.__bool__() has not been implemented.");
    }

    public org.python.Object __getattribute__(java.lang.String name) {
        throw new org.python.exceptions.NotImplementedError("float.__getattribute__() has not been implemented.");
    }

    public void __setattr__(java.lang.String name, org.python.Object value) {
        throw new org.python.exceptions.NotImplementedError("float.__setattr__() has not been implemented.");
    }

    public void __delattr__(java.lang.String name) {
        throw new org.python.exceptions.NotImplementedError("float.__delattr__() has not been implemented.");
    }

    public org.python.types.List __dir__() {
        throw new org.python.exceptions.NotImplementedError("float.__dir__() has not been implemented.");
    }

    public org.python.Object __add__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__add__() has not been implemented.");
    }

    public org.python.Object __sub__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__sub__() has not been implemented.");
    }

    public org.python.Object __mul__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__mul__() has not been implemented.");
    }

    public org.python.Object __truediv__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__truediv__() has not been implemented.");
    }

    public org.python.Object __floordiv__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__floordiv__() has not been implemented.");
    }

    public org.python.Object __mod__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__mod__() has not been implemented.");
    }

    public org.python.Object __divmod__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__divmod__() has not been implemented.");
    }

    public org.python.Object __pow__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__pow__() has not been implemented.");
    }

    public org.python.Object __radd__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__radd__() has not been implemented.");
    }

    public org.python.Object __rsub__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__rsub__() has not been implemented.");
    }

    public org.python.Object __rmul__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__rmul__() has not been implemented.");
    }

    public org.python.Object __rtruediv__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__rtruediv__() has not been implemented.");
    }

    public org.python.Object __rfloordiv__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__rfloordiv__() has not been implemented.");
    }

    public org.python.Object __rmod__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__rmod__() has not been implemented.");
    }

    public org.python.Object __rdivmod__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__rdivmod__() has not been implemented.");
    }

    public org.python.Object __rpow__(org.python.Object other) {
        throw new org.python.exceptions.NotImplementedError("float.__rpow__() has not been implemented.");
    }

    public org.python.Object __neg__() {
        throw new org.python.exceptions.NotImplementedError("float.__neg__() has not been implemented.");
    }

    public org.python.Object __pos__() {
        throw new org.python.exceptions.NotImplementedError("float.__pos__() has not been implemented.");
    }

    public org.python.Object __abs__() {
        if (this.value < 0.0) {
            return new org.python.types.Float(-this.value);
        } else {
            return new org.python.types.Float(this.value);
        }
    }

    public org.python.types.Int __int__() {
        return new org.python.types.Int((int) this.value);
    }

    public org.python.types.Float __float__() {
        return new org.python.types.Float(this.value);
    }

    public org.python.Object __round__() {
        throw new org.python.exceptions.NotImplementedError("float.__round__() has not been implemented.");
    }


}