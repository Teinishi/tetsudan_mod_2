-- include sfx 0 "m_tns_tetsudan_controller_3.ogg"

local PIVOT = {0, 0.05, 0.03}
local STEP_START = -1
local STEP_POS = {
	{0, 0.125, -0.005},
	{0, 0.125, 0.03},
	{0, 0.125, 0.065},
}

local STEP_LAST = STEP_START + #STEP_POS - 1
local STEP_ANGLES = {}
for i, v in ipairs(STEP_POS) do
	STEP_ANGLES[i + STEP_START - 1] = math.atan(v[3] - PIVOT[3], v[2] - PIVOT[2])
end

function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

local pos = nil
local theta = nil
local transform = matrix.identity()

function update()
	if not pos then return end
	local theta_tgt = STEP_ANGLES[clamp(pos, STEP_START, STEP_LAST)]
	theta = theta ~= nil and lerp(theta, theta_tgt, 0.4) or theta_tgt
	transform = matrix.translation(-PIVOT[1], -PIVOT[2], -PIVOT[3])
	transform = matrix.multiply(matrix.rotationX(theta), transform)
	transform = matrix.multiply(matrix.translation(PIVOT[1], PIVOT[2], PIVOT[3]), transform)
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
			component.sfxPlayOnce(0, 0, 0, 0, 0, 1, 6, 1, 1, 0.5)
		end
		pos = npos
		update()
	end
end

function onRender()
	component.renderMesh0(transform)
end
