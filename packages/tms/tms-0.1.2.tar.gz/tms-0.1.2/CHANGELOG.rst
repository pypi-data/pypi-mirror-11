CHANGELOG
=========

0.1.2 (released 2015-09-01)
---------------------------

- Added shortcuts for common builtin types, so you can now write ``tms.Int()``
  instead of ``tms.InstanceOf(int)``.

- Added ``tms.Passes``. This takes an arbitrary function that is expected
  to return a boolean,
  eg ``assert random.randrange(1, 3) == tms.Passes(lambda x: 1 <= x < 3)``.
  This is integrated with ``tms.InstanceOf`` and ``tms.Anything``,
  so you can write eg
  ``tms.InstanceOf(MyClass, lambda x: x.name.startswith('foo'))``.

0.1.1
-----

- Initial release

