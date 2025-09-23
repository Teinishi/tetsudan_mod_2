-- include sfx 0 "m_tns_tetsudan_controller_1.ogg"
-- include sfx 1 "m_tns_tetsudan_controller_2.ogg"

local PIVOT = {0, 0.029167, -0.125}
local STEP_START = -8
local STEP_LAST = 4
local STEP_ANGLES = {33, 21, 11, 4, -3, -9, -15, -21, -29, -36, -46, -56, -66}
for i, v in ipairs(STEP_ANGLES) do
	STEP_ANGLES[i] = math.rad(v)
end

function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

local pos = nil
local theta = nil
local transform0 = matrix.identity()

function update()
	if not pos then return end
	local theta_tgt = STEP_ANGLES[clamp(pos, STEP_START, STEP_LAST) - STEP_START + 1]
	theta = theta ~= nil and lerp(theta, theta_tgt, 0.4) or theta_tgt
	transform0 = matrix.translation(-PIVOT[1], -PIVOT[2], -PIVOT[3])
	transform0 = matrix.multiply(matrix.rotationX(theta), transform0)
	transform0 = matrix.multiply(matrix.translation(PIVOT[1], PIVOT[2], PIVOT[3]), transform0)
end

function onParse()
	pos, _ = parser.parseNumber("pos", pos)
	update()
end

function onTick()
	local value, success = component.getInputLogicSlotFloat(0)
	if success then
		local npos = clamp(math.floor(value + 0.5), STEP_START, STEP_LAST)
		if pos ~= nil and npos ~= pos then
			if npos == 0 or npos == STEP_START then
				component.sfxPlayOnce(1, 1, 0, 0, 0, 1, 6, 1, 1, 0.5)
			end
			component.sfxPlayOnce(0, 0, 0, 0, 0, 1, 6, 1, 1, 0.5)
		end
		pos = npos
		update()
	end
end

function onRender()
	component.renderMesh0(transform0)

end
