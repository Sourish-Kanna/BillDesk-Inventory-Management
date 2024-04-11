import modules.Install as Ins

Ins.install()
try:
    import PIL
except:
    raise SystemExit


from modules.Help import Help
Help()
