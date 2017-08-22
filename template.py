# Templates
Template('TransformComplex',
    "{pfx}_r{n}: {mf if mf is not None else m1+m2} -> {m1} + {m2};"
    + " cell*({pfx}_r{n}_k1*{mf if mf is not None else m1+m2}"
    + " - {pfx}_r{n}_k2*{m1}*{m2});")

Template("AddMoiety",
    "{pfx}_r{n}: {m1} => {m1}{m2}; cell*{pfx}_r{n}_k1*{m1};")

Template("RemoveMoiety",
    "{pfx}_r{n}: {m1}{m2} => {m1}; cell*{pfx}_r{n}_k1*{m1}{m2};")

Template("RemoveMoietyWithCatalyst",
    "{pfx}_r{n}: {m1}{m2} + {m3} => {m1} + {m3}; cell*{pfx}_r{n}_k1*{m1}{m2}*{m3};")

Template("TransferMoiety",
    "{pfx}_r{n}: {m1} + {m2}{m3} => {m1}{m3} + {m2}; cell*{pfx}_r{n}_k1*{m1}*{m2}{m3};")

Template("Constant2",'''
{pfx}_r{n}_k1 = {k1v};
{pfx}_r{n}_k1 has {k1u};
{pfx}_r{n}_k2 = {k2v};
{pfx}_r{n}_k2 has {k2u};'''

Template("Constant1",'''
{pfx}_r{n}_k1 = {k1v};
{pfx}_r{n}_k1 has {k1u};'''
