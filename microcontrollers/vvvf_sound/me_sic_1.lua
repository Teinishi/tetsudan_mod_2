local cch, sch = property.getNumber"Motor Current Ch.", property.getNumber"Speed Ch."
local VOLUME = property.getNumber"VVVF Sound Volume"

local abs, min, max = math.abs, math.min, math.max
function onTick()
	local c, s = input.getNumber(cch), input.getNumber(sch)*3.6
	local volume, pitch = {}, {}
	if abs(c) > 0 then
		volume[1] = min(min(2.5*s, 0.5), -1*s + 44.5)
		pitch[1] = 1
		if s < 45 then
			volume[2] = min(0.5*s, 1)
		end
		pitch[2] = 1
		volume[3] = -0.2*s + 3
		pitch[3] = 0.15432*s
		volume[4] = -0.071429*s + 3.1429
		pitch[4] = 0.041667*s
		if s < 45 then
			volume[5] = min(0.25*s - 4, 1)
		end
		pitch[5] = 0.027778*s
		if 45 <= s then
			volume[6] = min(1, -0.1*s + 6)
		end
		pitch[6] = 0.019183*s
		if 45 <= s then
			volume[7] = min(1, -0.05*s + 5.25)
		end
		pitch[7] = 0.013889*s
		volume[8] = 0.05*s - 3.5
		pitch[8] = 0.0086806*s
	end
	for i = 1, 8 do
		output.setNumber(2*i - 1, min(max((volume[i] or 0)*VOLUME, 0), 1))
		output.setNumber(2*i, max(pitch[i] or 0, 0))
	end
end
