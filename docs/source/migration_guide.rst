Migration Guide
===============

This guide helps you to easily migrate to ConfZ 2, which supports pydantic 2 and
improves naming conventions.

New Class Names
---------------

We renamed many classes to better reflect their purpose instead of being tied to the
package name. The following table summarizes all changes. Please make sure you adjust
your imports accordingly.

====================  ===============
ConfZ v1              ConfZ v2
====================  ===============
ConfZ                 BaseConfig
ConfZSource           ConfigSource
ConfZSources          ConfigSources
ConfZCLArgSource      CLArgSource
ConfZDataSource       DataSource
ConfZEnvSource        EnvSource
ConfZFileSource       FileSource
ConfZException        ConfigException
ConfZUpdateException  UpdateException
ConfZFileException    FileException
====================  ===============

Pydantic v2
-----------

Once initialized, a confz BaseConfig class behaves mostly like a regular pydantic
BaseModel class. Pydantic 2 comes with quite some changes, which might affect your code,
depending on the used functionalities. Check out the
`migration guide <https://docs.pydantic.dev/latest/migration/>`_.
