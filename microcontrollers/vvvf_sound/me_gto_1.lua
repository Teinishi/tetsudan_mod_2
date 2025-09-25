local cch, sch = property.getNumber"Motor Current Ch.", property.getNumber"Speed Ch."
local VOLUME = property.getNumber"VVVF Sound Volume"

local abs, min, max = math.abs, math.min, math.max
function onTick()
	local c, s = input.getNumber(cch), input.getNumber(sch)*3.6
	local volume, pitch = {}, {}
	if abs(c) > 0 then
		if s < 33.939 then
			volume[1] = 1
		end
		pitch[1] = min(0.058313*s + 0.70642, -5.8676e-6*s + 1.4121)
		if s < 43.03 then
			volume[2] = min(0.013045*s + 0.48259, 0.0040561*s + 0.6328)
		elseif s < 63.174 then
			volume[2] = 0.0045653*s + 0.61089
		else
			volume[2] = min(-0.0048766*s + 1.2074, -0.033122*s + 3.4665)
		end
		pitch[2] = 0.020533*s
		if 33.936 <= s and s < 45.714 then
			volume[3] = min(-0.033743*s + 2.1451, -0.063174*s + 3.4243)
		elseif s < 50.823 then
			volume[3] = -0.014147*s + 1.183
		elseif s < 70.563 then
			volume[3] = -0.016067*s + 1.2806
		else
			volume[3] = -0.006841*s + 0.6296
		end
		pitch[3] = 0.027325*s
		if s < 45.801 then
			volume[4] = max(0, 1.4074e14*s - 6.4459e15)
		elseif s < 72.035 then
			volume[4] = min(-0.027717*s + 2.2695, -0.049367*s + 3.6959)
		else
			volume[4] = -0.0076523*s + 0.69103
		end
		pitch[4] = 0.022087*s
		if s < 80.952 then
			volume[5] = max(0.018044*s - 0.59366, 0.026671*s - 1.159)
		else
			volume[5] = 1
		end
		if s < 74.978 then
			pitch[5] = max(7.9957e-4*s + 0.69364, 0.013508*s + 0.05988)
		else
			pitch[5] = min(0.0094351*s + 0.36525, 0.0059325*s + 0.70732)
		end
	end
	for i = 1, 5 do
		output.setNumber(2*i - 1, min(max((volume[i] or 0)*VOLUME, 0), 1))
		output.setNumber(2*i, max(pitch[i] or 0, 0))
	end
end
