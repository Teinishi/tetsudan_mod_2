local abs, min, max = math.abs, math.min, math.max
local pN, gN, sN = property.getNumber, input.getNumber, output.setNumber
local cch, sch = pN"Motor Current Ch.", pN"Speed Ch."
function onTick()
	local c, s = gN(cch), gN(sch)*3.6
	local volume, pitch = {}, {}
	if abs(c) > 0 then
		if 20 <= s then
			volume[3] = min(1, -0.33333*s + 10)
		end
		pitch[3] = 0.041481*s
		volume[4] = min(min(0.4*s - 10.4, 1), -0.5*s + 16.5)
		pitch[4] = 0.032593*s
		volume[5] = min(min(0.33333*s - 9.6667, 1), -0.19078*s + 8.2089)
		pitch[5] = 0.032286*s
		volume[6] = min(min(0.19571*s - 7.0714, 1), -0.087403*s + 6.1977)
		pitch[6] = 0.023256*s
		volume[7] = 0.062065*s - 3.1212
		pitch[7] = 0.011765*s
	end
	if c > 0 then
		volume[1] = -0.035087*s + 2.3809
		pitch[1] = 1
		if s < 20 then
			volume[2] = 0.0081481*s + 0.83704
		end
		pitch[2] = max(5e-3*s + 0.77, 0.022778*s + 0.73444)
	elseif c < 0 then
		if 7.5 <= s then
			volume[1] = min(1, -0.035087*s + 2.3809)
		end
		pitch[1] = 1
		if 7.5 <= s and s < 20 then
			volume[2] = 0.0081481*s + 0.83704
		end
		pitch[2] = max(max(0.0025*s + 0.77, 0.025625*s + 0.6775), 0.025625*s + 0.6775)
	end
	for i = 1, 7 do
		sN(2*i - 1, min(max(volume[i] or 0, 0), 1))
		sN(2*i, max(pitch[i] or 0, 0))
	end
end
