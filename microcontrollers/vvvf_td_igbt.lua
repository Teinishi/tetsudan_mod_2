local abs, min, max = math.abs, math.min, math.max
local pN, gN, sN = property.getNumber, input.getNumber, output.setNumber
local cch, sch = pN"Motor Current Ch.", pN"Speed Ch."
function onTick()
	local c, s = gN(cch), gN(sch)*3.6
	local volume, pitch = {}, {}
	if abs(c) > 0 then
		volume[1] = min(0.3, -0.3*s + 7.8)
		pitch[1] = 1
		volume[2] = min(min(0.175*s, 0.013953*s + 0.64419), -2*s + 52)
		pitch[2] = 1
		volume[3] = -0.16087*s + 3.0217
		pitch[3] = 0.066667*s
		volume[4] = min(min(0.13901*s - 1.2918, 1), -0.24667*s + 7.2333)
		pitch[4] = 0.045455*s
		volume[5] = min(min(2*s - 51, 1), -0.11111*s + 5.5556)
		pitch[5] = 0.033333*s
		volume[6] = 0.065152*s - 1.7487
		pitch[6] = 0.015385*s
	end
	for i = 1, 6 do
		sN(2*i - 1, min(max(volume[i] or 0, 0), 1))
		sN(2*i, max(pitch[i] or 0, 0))
	end
end
