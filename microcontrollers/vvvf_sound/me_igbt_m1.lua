local cch, sch = property.getNumber"Motor Current Ch.", property.getNumber"Speed Ch."
local VOLUME = property.getNumber"VVVF Sound Volume"

local abs, min, max = math.abs, math.min, math.max
function onTick()
	local c, s = input.getNumber(cch), input.getNumber(sch)*3.6
	local volume, pitch = {}, {}
	if abs(c) > 0 then
		if s < 7 then
			volume[1] = max(0, 1*s - 6)
		elseif s < 47.647 then
			volume[1] = min(1, -0.0067388*s + 1.2278)
		elseif s < 53.704 then
			volume[1] = 0.015408*s + 0.17256
		else
			volume[1] = min(1, -0.016794*s + 2.025)
		end
		pitch[1] = 0.016065*s
		volume[5] = 0
		pitch[5] = 1
	end
	if c > 0 then
		if 35 <= s and s < 47.3 then
			volume[2] = min(1, -0.083247*s + 4.2966)
		elseif s < 53.6 then
			volume[2] = 0.10175*s - 4.4536
		else
			volume[2] = 1
		end
		pitch[2] = 0.019884*s
		if 39.6 <= s then
			volume[3] = min(1, -0.0052055*s + 1.3758)
		end
		pitch[3] = 0.01359*s
		if s < 35 then
			volume[6] = -0.04*s + 1.8
		end
		if s < 5.5 then
			pitch[6] = max(0.48, 0.26*s - 0.43)
		else
			pitch[6] = 1
		end
	elseif c < 0 then
		if 40 <= s and s < 44.644 then
			volume[2] = min(1, -1.2467*s + 56.352)
		else
			volume[2] = 0.034076*s - 0.8259
		end
		pitch[2] = 0.019884*s
		if 44.6 <= s then
			volume[3] = min(0.01087*s + 0.21519, -0.0051792*s + 1.3739)
		end
		pitch[3] = 0.013602*s
		volume[4] = -1*s + 3.2
		pitch[4] = 1
		if s < 40 then
			volume[6] = min(min(1*s - 2.2, 1), -0.03*s + 1.6)
		end
		if s < 5.5 then
			pitch[6] = max(0.19, 0.27*s - 0.485)
		else
			pitch[6] = 1
		end
	end
	for i = 1, 6 do
		output.setNumber(2*i - 1, min(max((volume[i] or 0)*VOLUME, 0), 1))
		output.setNumber(2*i, max(pitch[i] or 0, 0))
	end
end
