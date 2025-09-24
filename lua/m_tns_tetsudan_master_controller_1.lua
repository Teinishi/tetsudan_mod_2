-- include sfx 0 "m_tns_tetsudan_controller_1.ogg"
-- include sfx 1 "m_tns_tetsudan_controller_2.ogg"

local PIVOT = {0, 0.05, 0}
local STEP_START = -9
local STEP_POS = {
	{0, 0.125, 0.072169},
	{0, 0.125, 0.057831},
	{0, 0.125, 0.047831},
	{0, 0.125, 0.038831},
	{0, 0.125, 0.029831},
	{0, 0.125, 0.021831},
	{0, 0.125, 0.013831},
	{0, 0.125, 0.005831},
	{0, 0.125, -0.002169},
	{0, 0.125, -0.012},
	{0, 0.125, -0.022169},
	{0, 0.125, -0.032169},
	{0, 0.125, -0.043169},
	{0, 0.125, -0.057169},
	{0, 0.125, -0.072169},
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
local btn_press = 0
local transform0, transform1 = matrix.identity(), matrix.identity()

function update()
	if not pos then return end
	local theta_tgt = STEP_ANGLES[clamp(pos, STEP_START, STEP_LAST)]
	if theta == theta_tgt then return end
	theta = theta ~= nil and lerp(theta, theta_tgt, 0.4) or theta_tgt
	btn_press = lerp(btn_press, pos > 0 and 1 or 0, 0.7)
	transform0 = matrix.translation(-PIVOT[1], -PIVOT[2], -PIVOT[3])
	transform0 = matrix.multiply(matrix.rotationX(theta), transform0)
	transform0 = matrix.multiply(matrix.translation(PIVOT[1], PIVOT[2], PIVOT[3]), transform0)
	transform1 = matrix.multiply(transform0, matrix.translation(-0.012*btn_press, 0, 0))
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
	component.renderMesh1(transform1)
end
