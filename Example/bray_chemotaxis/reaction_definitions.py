import collections
"""
rn is the reaction number
m1, m2, m3 are molecules in the reaction
k1, k2 are kinetics constants
"""
CF = collections.namedtuple('CF', 'nm m1 m2')  # Complex formation
CD = collections.namedtuple('CD', 'nm m1 m2')  # Complex disassociation
MT = collections.namedtuple('MT', 'nm m1 m2 m3')  # Moiety transfer
MA = collections.namedtuple('MA', 'nm m1 m2')  # Moiety addition
MR = collections.namedtuple('MR', 'nm m1 m2')  # Moiety removal
BMR = collections.namedtuple('BMR', 'nm m1 m2 m3')  # Biomolecular moiety removal
cd_definitions = [ 
                   CD(1,  'TT',    'W'),   
                   CD(2,  'W',     'AA'),   
                   CD(3,  'TT',    'WAA'),   
                   CD(4,  'TTW',   'WAA'),   
                   CD(5,  'TTWW',  'AA'),   
                   CD(6,  'TT',    'WWAA'),   
                   CD(7,  'TT',    'AA'),   
                   CD(8,  'TTW',   'AA'),   
                   CD(9,  'TTWAA', 'W'),   
                   CD(10, 'TTW',   'W'),   
                   CD(11, 'W',     'WAA'),   
                   CD(12, 'TTAA',  'W')
                  ]
mr_definitions = [
                  MR(8,  'Y', 'p'), 
                  MR(10, 'B', 'p'), 
                 ]
bmr_definitions = [
                   BMR(9,  'Y', 'p', 'Z'), 
                  ]
ma_definitions = [
                  MA(1, 'TTWWAA', 'p'), 
                  MA(2, 'AA',     'p'), 
                  MA(3, 'WAA',    'p'), 
                  MA(4, 'WWAA',   'p'), 
                  MA(5, 'TTAA',   'p'), 
                  MA(6, 'TTWAA',  'p'), 
                  MA(7, 'Y',      'p'), 
                 ]
tuples = [
          (1, 'AA',), 
          (2, 'WAA'), 
          (3, 'WWAA'),
          (4, 'TTAA'),
          (5, 'TTWAA'),
          (6, 'TTWWAA')
         ]
mt_definitions = [MT(t[0], 'B', t[1], 'p') for t in tuples]
mt_definitions.extend([MT(t[0] + 6, 'Y', t[1], 'p') for t in tuples])
