-- include sfx 0 "m_tns_tetsudan_controller_3.ogg"

local PIVOT = {0.07, -0.21178, 0.0}
local STEP_ANGLES = {-20, 0, 20}
local STEP_START = -1
local PLATE_Y = -0.10875

local mat_pivot = matrix.translation(PIVOT[1], PIVOT[2], PIVOT[3])
local mat_pivot_neg = matrix.translation(-PIVOT[1], -PIVOT[2], -PIVOT[3])
local step_angles_rad = {}
for i, v in ipairs(STEP_ANGLES) do
	step_angles_rad[STEP_START + i - 1] = math.rad(v)
end

function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

local pos = nil
local theta = nil
local transform1, transform2 = matrix.identity(), matrix.identity()

function update(npos)
	if npos == nil then return end
	pos = npos
	local theta_tgt = step_angles_rad[pos]
	if theta_tgt == nil or theta == theta_tgt then return end
	if theta == nil or math.abs(theta_tgt - theta) < 1e-4 then
		theta = theta_tgt
	else
		theta = lerp(theta, theta_tgt, 0.4)
	end
	transform1 = matrix.multiply(matrix.rotationX(theta), mat_pivot_neg)
	transform1 = matrix.multiply(mat_pivot, transform1)
	transform2 = matrix.translation(0, 0, math.tan(theta)*(PLATE_Y - PIVOT[2]))
end

function onTick()
	local value, success = component.getInputLogicSlotFloat(0)
	if success then
		local npos = clamp(math.floor(value + 0.5), STEP_START, STEP_START + #STEP_ANGLES - 1)
		if pos ~= nil and npos ~= pos then
			component.sfxPlayOnce(0, 0, 0, 0, 0, 1, 6, 1, 1, 0.5)
		end
		update(npos)
	end
end

function onRender()
	component.renderMesh0(transform1)
	component.renderMesh1(transform2)
end
