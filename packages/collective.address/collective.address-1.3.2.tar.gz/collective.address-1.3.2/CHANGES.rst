Changelog
=========

1.3.2 (2015-09-24)
------------------

- Encode SearchableText indexer result in utf-8.
  [thet]


1.3.1 (2015-08-27)
------------------

- Fix error on creating the title for Person types with non-ascii characters in
  names.
  [thet]


1.3 (2015-07-21)
----------------

- Let IAddressable not derive from schema.Model to have a pure marker
  Interface.
  [thet]

- Make sure, all SearchableText parts are seperated by a space.
  [thet]


1.2 (2015-07-15)
----------------

- Require the last_name attribute of IPerson behavior.
  [thet]

- For the IPerson behavior, compute the title from first and last name and add
  title (not required, hidden) and description to the IPerson behavior.
  [thet]


1.1 (2015-03-04)
----------------

- Add IContact and IPerson behaviors in addition to the IAddress behavior.
  [thet]

- PEP 8.
  [thet]


1.0 (2014-04-30)
----------------

- initial.
