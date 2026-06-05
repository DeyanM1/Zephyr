# Zephyr Library Manager

Zephyr uses the Zephyr Library Manager, zlm.py, to install and remove libraries. The tool handles local and global library storage and keeps project dependencies organized.

## Installing Libraries

Use the install command to add one or more libraries.

```
zlm.py install --path "src/lib/" GPIO.py moreMath.py ...
```

The command installs libraries into the specified directory. If you omit the path option, zlm.py installs libraries into lib inside the current working directory. Use the --global flag to install libraries system wide. Global installation stays disabled by default.

Example global install.

```
zlm.py install --global GPIO.py
```

## Uninstalling Libraries

Use the uninstall command to remove a library.

```
zlm.py uninstall GPIO.py
```

Uninstall always targets global libraries. Local project libraries require manual removal from the project directory.

## Notes on Usage

Use local installation for project specific dependencies. Use global installation for shared libraries across multiple Zephyr projects. Keep library names exact, including file extensions, to avoid resolution errors.