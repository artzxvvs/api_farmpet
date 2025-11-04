import traceback

logfile = 'diag_import.log'
with open(logfile, 'w', encoding='utf-8') as f:
    try:
        import main
        f.write('import main: OK\n')
        try:
            app = main.app
            f.write('main.app exists\n')
            try:
                schema = app.openapi()
                f.write('openapi len: %d\n' % len(str(schema)))
            except Exception:
                f.write('ERROR generating openapi:\n')
                traceback.print_exc(file=f)
        except Exception:
            f.write('ERROR accessing main.app:\n')
            traceback.print_exc(file=f)
    except Exception:
        f.write('ERROR importing main:\n')
        traceback.print_exc(file=f)
print('Wrote', logfile)
