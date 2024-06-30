.data
str_nl: .asciz "\n"
.text

L_100:
j L_main
L_101:
#101: begin_block, max3, _, _
sw ra,(sp)
L_102:
#102: +, counterFunctionCalls, 1, T$0
lw t1,-12(gp)
li t2, 1
add t1,t1,t2
sw t1,-28(sp)
L_103:
#103: =, T$0, _, counterFunctionCalls
lw t1,-28(sp)
sw t1,-12(gp)
L_104:
#104: >, x, y, 106
lw t1,-12(sp)
lw t2,-16(sp)
bgt, t1, t2, L_106
L_105:
#105: jump , _, _, 110
j L_110
L_106:
#106: >, x, z, 108
lw t1,-12(sp)
lw t2,-20(sp)
bgt, t1, t2, L_108
L_107:
#107: jump , _, _, 110
j L_110
L_108:
#108: =, x, _, m
lw t1,-12(sp)
sw t1,-24(sp)
L_109:
#109: jump , _, _, 117
j L_117
L_110:
#110: >, y, x, 112
lw t1,-16(sp)
lw t2,-12(sp)
bgt, t1, t2, L_112
L_111:
#111: jump , _, _, 116
j L_116
L_112:
#112: >, y, z, 114
lw t1,-16(sp)
lw t2,-20(sp)
bgt, t1, t2, L_114
L_113:
#113: jump , _, _, 116
j L_116
L_114:
#114: =, y, _, m
lw t1,-16(sp)
sw t1,-24(sp)
L_115:
#115: jump , _, _, 117
j L_117
L_116:
#116: =, z, _, m
lw t1,-20(sp)
sw t1,-24(sp)
L_117:
#117: ret, m, _, _
lw t0,-8(sp)
lw t1,-24(sp)
sw t1,(t0)
lw ra, (sp)
jr ra
L_118:
#118: end_block, max3, _, _
lw ra,(sp)
jr ra
L_119:
#119: begin_block, divides, _, _
sw ra,(sp)
L_120:
#120: +, counterFunctionCalls, 1, T$1
lw t1,-12(gp)
li t2, 1
add t1,t1,t2
sw t1,-16(sp)
L_121:
#121: =, T$1, _, counterFunctionCalls
lw t1,-16(sp)
sw t1,-12(gp)
L_122:
#122: //, y, x, T$2
lw t1,-12(sp)
div t1,t1,t2
sw t1,-20(sp)
L_123:
#123: *, T$2, x, T$3
lw t1,-20(sp)
mul t1,t1,t2
sw t1,-24(sp)
L_124:
#124: ==, y, T$3, 126
lw t1,-12(sp)
lw t2,-24(sp)
beq, t1, t2, L_126
L_125:
#125: jump , _, _, 127
j L_127
L_126:
#126: ret, 1, _, _
lw t0,-8(sp)
li t1, 1
sw t1,(t0)
lw ra, (sp)
jr ra
L_127:
#127: ret, 0, _, _
lw t0,-8(sp)
li t1, 0
sw t1,(t0)
lw ra, (sp)
jr ra
L_128:
#128: end_block, divides, _, _
lw ra,(sp)
jr ra
L_129:
#129: begin_block, isPrime, _, _
sw ra,(sp)
L_130:
#130: +, counterFunctionCalls, 1, T$4
lw t1,-12(gp)
li t2, 1
add t1,t1,t2
sw t1,-20(sp)
L_131:
#131: =, T$4, _, counterFunctionCalls
lw t1,-20(sp)
sw t1,-12(gp)
L_132:
#132: =, 2, _, i
li t1, 2
sw t1,-16(sp)
L_133:
#133: <, i, x, 135
lw t1,-16(sp)
lw t2,-12(sp)
blt, t1, t2, L_135
L_134:
#134: jump , _, _, 145
j L_145
L_135:
#135: par, i, CV, _
addi fp, sp, 28
L_136:
#136: par, x, CV, _
addi fp, sp, 28
L_137:
#137: par, T$5, RET, _
addi fp, sp, 28
L_138:
#138: call, _, _, divides
sw sp , -4(fp)
addi sp, sp, 28
jal L_119
addi sp, sp, -28
L_139:
#139: ==, T$5, 1, 141
lw t1,-24(sp)
li t2, 1
beq, t1, t2, L_141
L_140:
#140: jump , _, _, 145
j L_145
L_141:
#141: ret, 0, _, _
lw t0,-8(sp)
li t1, 0
sw t1,(t0)
lw ra, (sp)
jr ra
L_142:
#142: +, i, 1, T$6
lw t1,-16(sp)
li t2, 1
add t1,t1,t2
sw t1,-28(sp)
L_143:
#143: =, T$6, _, i
lw t1,-28(sp)
sw t1,-16(sp)
L_144:
#144: jump , _, _, 133
j L_133
L_145:
#145: ret, 1, _, _
lw t0,-8(sp)
li t1, 1
sw t1,(t0)
lw ra, (sp)
jr ra
L_146:
#146: end_block, isPrime, _, _
lw ra,(sp)
jr ra
L_147:
#147: begin_block, sqr, _, _
sw ra,(sp)
L_148:
#148: +, counterFunctionCalls, 1, T$7
lw t1,-12(gp)
li t2, 1
add t1,t1,t2
sw t1,-12(sp)
L_149:
#149: =, T$7, _, counterFunctionCalls
lw t1,-12(sp)
sw t1,-12(gp)
L_150:
#150: *, x, x, T$8
mul t1,t1,t2
sw t1,-16(sp)
L_151:
#151: =, T$8, _, T$9
lw t1,-16(sp)
sw t1,-20(sp)
L_152:
#152: ret, T$9, _, _
lw t0,-8(sp)
lw t1,-20(sp)
sw t1,(t0)
lw ra, (sp)
jr ra
L_153:
#153: end_block, sqr, _, _
lw ra,(sp)
jr ra
L_154:
#154: begin_block, quad, _, _
sw ra,(sp)
L_155:
#155: =, 3, _, x
li t1, 3
sw t1,-12(sp)
L_156:
#156: +, counterFunctionCalls, 1, T$10
lw t1,-12(gp)
li t2, 1
add t1,t1,t2
sw t1,-20(sp)
L_157:
#157: =, T$10, _, counterFunctionCalls
lw t1,-20(sp)
sw t1,-12(gp)
L_158:
#158: par, x, CV, _
addi fp, sp, 24
L_159:
#159: par, T$11, RET, _
addi fp, sp, 24
L_160:
#160: call, _, _, sqr
sw sp , -4(fp)
addi sp, sp, 24
jal L_147
addi sp, sp, -24
L_161:
#161: par, x, CV, _
addi fp, sp, 24
L_162:
#162: par, T$12, RET, _
addi fp, sp, 24
L_163:
#163: call, _, _, sqr
sw sp , -4(fp)
addi sp, sp, 24
jal L_147
addi sp, sp, -24
L_164:
#164: *, T$11, T$12, T$13
lw t1,-24(sp)
lw t2,-28(sp)
mul t1,t1,t2
sw t1,-32(sp)
L_165:
#165: =, T$13, _, y
lw t1,-32(sp)
sw t1,-16(sp)
L_166:
#166: ret, y, _, _
lw t0,-8(sp)
lw t1,-16(sp)
sw t1,(t0)
lw ra, (sp)
jr ra
L_167:
#167: end_block, quad, _, _
lw ra,(sp)
jr ra
L_168:
L_main:
#168: begin_block, main, _, _
addi sp, sp, 36
mv s0 sp
sw ra,(sp)
L_169:
#169: =, 0, _, counterFunctionCalls
li t1, 0
sw t1,-12(sp)
L_170:
#170: input, _, _, i
li a7, 5
ecall
sw a0,-16(sp)
L_171:
#171: print, i, _, _
lw a0,-16(sp)
li a7,1
ecall
la a0,str_nl
li a7,4
ecall
L_172:
#172: =, 1600, _, i
li t1, 1600
sw t1,-16(sp)
L_173:
#173: <=, i, 2000, 175
lw t1,-16(sp)
li t2, 2000
ble, t1, t2, L_175
L_174:
#174: jump , _, _, 178
j L_178
L_175:
#175: +, i, 400, T$14
lw t1,-16(sp)
li t2, 400
add t1,t1,t2
sw t1,-20(sp)
L_176:
#176: =, T$14, _, i
lw t1,-20(sp)
sw t1,-16(sp)
L_177:
#177: jump , _, _, 173
j L_173
L_178:
#178: par, 173, CV, _
addi fp, sp, 36
L_179:
#179: par, T$15, RET, _
addi fp, sp, 36
L_180:
#180: call, _, _, quad
sw sp , -4(fp)
addi sp, sp, 36
jal L_154
addi sp, sp, -36
L_181:
#181: print, T$15, _, _
lw a0,-24(sp)
li a7,1
ecall
la a0,str_nl
li a7,4
ecall
L_182:
#182: =, 1, _, i
li t1, 1
sw t1,-16(sp)
L_183:
#183: <=, i, 12, 185
lw t1,-16(sp)
li t2, 12
ble, t1, t2, L_185
L_184:
#184: jump , _, _, 192
j L_192
L_185:
#185: par, i, CV, _
addi fp, sp, 32
L_186:
#186: par, T$16, RET, _
addi fp, sp, 32
L_187:
#187: call, _, _, isPrime
sw sp , -4(fp)
addi sp, sp, 32
jal L_129
addi sp, sp, -32
L_188:
#188: print, T$16, _, _
lw a0,-28(sp)
li a7,1
ecall
la a0,str_nl
li a7,4
ecall
L_189:
#189: +, i, 1, T$17
lw t1,-16(sp)
li t2, 1
add t1,t1,t2
sw t1,-32(sp)
L_190:
#190: =, T$17, _, i
lw t1,-32(sp)
sw t1,-16(sp)
L_191:
#191: jump , _, _, 183
j L_183
L_192:
#192: print, counterFunctionCalls, _, _
lw a0,-12(sp)
li a7,1
ecall
la a0,str_nl
li a7,4
ecall
L_193:
#193: halt, _, _, _
li a0, 0
li a7, 93
ecall
L_194:
#194: end_block, main, _, _
lw ra,(sp)
jr ra
